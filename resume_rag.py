from fs_tools import read_file
from sentence_transformers import SentenceTransformer
import chromadb
import re
import os

# Common resume section headings
SECTION_HEADINGS = [
    "PROFESSIONAL SUMMARY",
    "SUMMARY",
    "OBJECTIVE",
    "SKILLS",
    "TECHNICAL SKILLS",
    "EXPERIENCE",
    "WORK EXPERIENCE",
    "PROFESSIONAL EXPERIENCE",
    "EDUCATION",
    "PROJECTS",
    "CERTIFICATIONS"
]


def split_resume_into_sections(text):
    """
    Split resume text into logical sections such as
    Skills, Experience and Education.
    """

    sections = {}
    current_section = "HEADER"
    sections[current_section] = []

    lines = text.splitlines()

    for line in lines:
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        # Check whether this line is a known section heading
        if cleaned_line.upper() in SECTION_HEADINGS:
            current_section = cleaned_line.upper()

            if current_section not in sections:
                sections[current_section] = []

        else:
            sections[current_section].append(cleaned_line)

    # Convert lists of lines into text
    final_sections = {}

    for section_name, section_lines in sections.items():
        if section_lines:
            final_sections[section_name] = "\n".join(section_lines)

    return final_sections

def create_chunks(sections, max_words=150):
    """
    Convert resume sections into smaller chunks while
    preserving the section name.

    Large sections are split into chunks of max_words.
    """

    chunks = []

    for section_name, section_content in sections.items():

        words = section_content.split()

        # Small section - keep it as one chunk
        if len(words) <= max_words:
            chunks.append({
                "section": section_name,
                "content": section_content
            })

        # Large section - split into smaller chunks
        else:
            for i in range(0, len(words), max_words):
                chunk_words = words[i:i + max_words]
                chunk_text = " ".join(chunk_words)

                chunks.append({
                    "section": section_name,
                    "content": chunk_text
                })

    return chunks




def extract_metadata(sections):
    """
    Extract important candidate information from resume sections.
    """

    metadata = {
        "name": "",
        "skills": [],
        "experience_years": 0,
        "education": ""
    }

    # -----------------------------------
    # 1. Extract candidate name
    # -----------------------------------
    if "HEADER" in sections:
        header_lines = sections["HEADER"].splitlines()

        if header_lines:
            metadata["name"] = header_lines[0].strip()

    # -----------------------------------
    # 2. Extract skills
    # -----------------------------------
    skills_section = None

    if "SKILLS" in sections:
        skills_section = sections["SKILLS"]
    elif "TECHNICAL SKILLS" in sections:
        skills_section = sections["TECHNICAL SKILLS"]

    if skills_section:
        skills = []

        for line in skills_section.splitlines():
            skill = line.strip()

            if skill:
                skills.append(skill)

        metadata["skills"] = skills

    # -----------------------------------
    # 3. Extract years of experience
    # -----------------------------------
    full_text = " ".join(sections.values())

    experience_match = re.search(
        r"(\d+)\+?\s+years?\s+of\s+experience",
        full_text,
        re.IGNORECASE
    )

    if experience_match:
        metadata["experience_years"] = int(
            experience_match.group(1)
        )

    # -----------------------------------
    # 4. Extract education
    # -----------------------------------
    if "EDUCATION" in sections:
        metadata["education"] = sections["EDUCATION"]

    return metadata



def generate_embeddings(chunks):
    """
    Generate vector embeddings for resume chunks.
    """

    print("\nLoading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = []

    for chunk in chunks:
        text = f"{chunk['section']}: {chunk['content']}"
        texts.append(text)

    embeddings = model.encode(texts)

    return embeddings



def store_in_chromadb(chunks, embeddings, metadata, resume_path):
    """
    Store resume chunks, embeddings and metadata in ChromaDB.
    """

    # Create persistent ChromaDB database
    client = chromadb.PersistentClient(path="chroma_db")

    # Create or get collection
    collection = client.get_or_create_collection(
        name="resume_collection",
        configuration={
            "hnsw": {
                "space": "cosine"
            }
        }
    )

    # Store every resume chunk
    for index, chunk in enumerate(chunks):

        filename = os.path.basename(resume_path)

        safe_filename = filename.replace(
            ".",
            "_"
        ).replace(
            " ",
            "_"
        )

        chunk_id = f"{safe_filename}_{index}"

        chunk_metadata = {
            "candidate_name": metadata["name"],
            "section": chunk["section"],
            "experience_years": metadata["experience_years"],
            "education": metadata["education"],
            "resume_path": resume_path,
            "skills": ", ".join(metadata["skills"])
        }

        collection.upsert(
            ids=[chunk_id],
            documents=[chunk["content"]],
            embeddings=[embeddings[index].tolist()],
            metadatas=[chunk_metadata]
        )

    return collection




def semantic_search(collection, query, top_k=3):
    """
    Search ChromaDB for resume chunks that are
    semantically similar to the query.
    """

    print("\nGenerating query embedding...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_embedding = model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results





def get_resume_files(directory="resumes"):
    """
    Find all supported resume files.
    """

    supported_extensions = (
        ".txt",
        ".pdf",
        ".docx"
    )

    resume_files = []

    for filename in os.listdir(directory):

        if filename.lower().endswith(
            supported_extensions
        ):
            full_path = os.path.join(
                directory,
                filename
            )

            resume_files.append(full_path)

    return resume_files







def main():

    print(
        "\n========== RESUME RAG INGESTION ==========\n"
    )

    resume_files = get_resume_files()

    print(
        f"Found {len(resume_files)} resume(s).\n"
    )

    if not resume_files:
        print("No resumes found.")
        return

    # Load embedding model once
    print("Loading embedding model...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    # Connect to ChromaDB once
    client = chromadb.PersistentClient(
        path="chroma_db"
    )

    collection = client.get_or_create_collection(
        name="resume_collection"
    )

    for resume_path in resume_files:

        print(
            f"\nProcessing: {resume_path}"
        )

        result = read_file(resume_path)

        if not result["success"]:
            print(
                f"Failed to read: {resume_path}"
            )
            continue

        resume_text = result["content"]

        sections = split_resume_into_sections(
            resume_text
        )

        chunks = create_chunks(sections)

        metadata = extract_metadata(sections)

        texts = []

        for chunk in chunks:
            text = (
                f"{chunk['section']}: "
                f"{chunk['content']}"
            )
            texts.append(text)

        embeddings = model.encode(texts)

        store_in_chromadb(
            chunks,
            embeddings,
            metadata,
            resume_path
        )

        print(
            f"Stored candidate: "
            f"{metadata['name']}"
        )

        print(
            f"Chunks stored: {len(chunks)}"
        )

    print(
        "\n========== INGESTION COMPLETE ==========\n"
    )

    print(
        f"Total ChromaDB records: "
        f"{collection.count()}"
    )

if __name__ == "__main__":
    main()