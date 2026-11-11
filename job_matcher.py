import chromadb
import re
import json
import os
import sys
from sentence_transformers import SentenceTransformer


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "resume_collection"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_database():
    """
    Connect to the existing ChromaDB database.
    """

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


def semantic_search(collection, job_description, top_k=5):
    """
    Find resume chunks semantically similar
    to the job description.
    """

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    job_embedding = model.encode(
        job_description
    )

    available_records = collection.count()

    n_results = min(
        top_k,
        available_records
    )

    results = collection.query(
        query_embeddings=[
            job_embedding.tolist()
        ],
        n_results=n_results
    )

    return results


def read_job_description(filepath):
    """
    Read job description from a text file.
    """

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()





def extract_required_skills(job_description):
    """
    Identify important technical skills mentioned
    in the job description.
    """

    known_skills = [
    "Python",
    "Java",
    "JavaScript",
    "FastAPI",
    "Django",
    "Flask",
    "Spring Boot",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",
    "Git",
    "Machine Learning",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "Spark",
    "Terraform",
    "Linux",
    "CI/CD"
]

    required_skills = []

    job_lower = job_description.lower()

    for skill in known_skills:
        if skill.lower() in job_lower:
            required_skills.append(skill)

    return required_skills







def calculate_skill_match(required_skills, candidate_skills):
    """
    Compare job skills with candidate skills and
    calculate a percentage match.
    """

    candidate_skills_lower = [
        skill.strip().lower()
        for skill in candidate_skills.split(",")
    ]

    matched_skills = []

    for skill in required_skills:
        if skill.lower() in candidate_skills_lower:
            matched_skills.append(skill)

    if not required_skills:
        return 0, []

    skill_score = (
        len(matched_skills) / len(required_skills)
    ) * 100

    return skill_score, matched_skills




def extract_required_experience(job_description):
    """
    Extract required years of experience
    from the job description.
    """

    match = re.search(
        r"(\d+)\+?\s+years",
        job_description,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return 0



def calculate_experience_score(
    required_years,
    candidate_years
):
    """
    Calculate experience requirement score.
    """

    if required_years == 0:
        return 100

    if candidate_years >= required_years:
        return 100

    return (
        candidate_years / required_years
    ) * 100






def distance_to_score(distance):
    """
    Convert vector distance to a simple
    0-100 semantic similarity score.
    """

    score = (1 - distance) * 100

    return max(0, min(100, score))






def calculate_hybrid_score(
    semantic_score,
    skill_score,
    experience_score
):
    """
    Combine semantic, skill and experience scores.
    """

    final_score = (
        semantic_score * 0.60
        + skill_score * 0.25
        + experience_score * 0.15
    )

    return round(final_score, 2)







def group_results_by_candidate(results):
    """
    Group retrieved resume chunks by candidate.
    """

    candidates = {}

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        candidate_name = metadata["candidate_name"]

        if candidate_name not in candidates:
            candidates[candidate_name] = {
                "metadata": metadata,
                "chunks": [],
                "distances": []
            }

        candidates[candidate_name]["chunks"].append(
            document
        )

        candidates[candidate_name]["distances"].append(
            distance
        )

    return candidates





def rank_candidates(
    grouped_candidates,
    required_skills,
    required_experience,
    must_have_skills
):
    """
    Calculate one final score for each candidate.
    """

    ranked_candidates = []

    for candidate_name, candidate_data in grouped_candidates.items():

        metadata = candidate_data["metadata"]
        distances = candidate_data["distances"]
        chunks = candidate_data["chunks"]


        requirement_check = check_must_have_requirements(
            candidate_data,
            must_have_skills,
            required_experience
        )


        # Use the best semantic match among the candidate's chunks
        best_distance = min(distances)

        semantic_score = distance_to_score(
            best_distance
        )

        skill_score, matched_skills = (
            calculate_skill_match(
                required_skills,
                metadata["skills"]
            )
        )

        experience_score = (
            calculate_experience_score(
                required_experience,
                metadata["experience_years"]
            )
        )

        final_score = calculate_hybrid_score(
            semantic_score,
            skill_score,
            experience_score
        )

        candidate_result = {
            "candidate_name": candidate_name,
            "resume_path": metadata["resume_path"],
            "match_score": final_score,
            "matched_skills": matched_skills,
            "experience_years": metadata["experience_years"],
            "relevant_excerpts": chunks[:3],
            "meets_must_have": requirement_check["passed"],
            "missing_skills": requirement_check["missing_skills"],
            "experience_requirement_met": requirement_check["experience_met"]
        }


        candidate_result["reasoning"] = (
            generate_match_reasoning(
                candidate_result,
                required_experience
            )
        )



        ranked_candidates.append(
            candidate_result
        )

    ranked_candidates.sort(
        key=lambda candidate: candidate["match_score"],
        reverse=True
    )

    return ranked_candidates





def check_must_have_requirements(
    candidate,
    must_have_skills,
    required_experience
):
    """
    Check whether candidate satisfies
    must-have job requirements.
    """

    candidate_skills = [
        skill.strip().lower()
        for skill in candidate["metadata"]["skills"].split(",")
    ]

    missing_skills = []

    for skill in must_have_skills:
        if skill.lower() not in candidate_skills:
            missing_skills.append(skill)

    experience_met = (
        candidate["metadata"]["experience_years"]
        >= required_experience
    )

    passed = (
        len(missing_skills) == 0
        and experience_met
    )

    return {
        "passed": passed,
        "missing_skills": missing_skills,
        "experience_met": experience_met
    }





def extract_must_have_skills(job_description):
    """
    Extract skills listed under the
    Required Skills section of the JD.
    """

    must_have_skills = []

    known_skills = [
    "Python",
    "Java",
    "JavaScript",
    "FastAPI",
    "Django",
    "Flask",
    "Spring Boot",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",
    "Git",
    "Machine Learning",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "Spark",
    "Terraform",
    "Linux",
    "CI/CD"
]

    match = re.search(
        r"Required Skills:(.*?)(?:Preferred Skills:|$)",
        job_description,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        required_section = match.group(1).lower()

        for skill in known_skills:
            if skill.lower() in required_section:
                must_have_skills.append(skill)

    return must_have_skills





def generate_match_reasoning(candidate, required_experience):
    """
    Generate simple explainable match reasoning.
    """

    matched_skills = candidate["matched_skills"]
    missing_skills = candidate["missing_skills"]
    experience_years = candidate["experience_years"]

    reasons = []

    if matched_skills:
        reasons.append(
            "Matched skills: "
            + ", ".join(matched_skills)
        )

    if experience_years >= required_experience:
        reasons.append(
            f"Meets the required {required_experience}+ "
            f"years of experience with "
            f"{experience_years} years."
        )
    else:
        reasons.append(
            f"Has only {experience_years} years of "
            f"experience; {required_experience}+ "
            f"years are required."
        )

    if missing_skills:
        reasons.append(
            "Missing must-have skills: "
            + ", ".join(missing_skills)
        )

    if candidate["meets_must_have"]:
        reasons.append(
            "Candidate satisfies all must-have requirements."
        )
    else:
        reasons.append(
            "Candidate does not satisfy all must-have requirements."
        )

    return " ".join(reasons)



def create_output(
    job_description,
    qualified_candidates,
    top_k=10
):
    """
    Create the final assignment output structure.
    """

    top_matches = []

    for candidate in qualified_candidates[:top_k]:

        match = {
            "candidate_name": candidate["candidate_name"],
            "resume_path": candidate["resume_path"],
            "match_score": candidate["match_score"],
            "matched_skills": candidate["matched_skills"],
            "relevant_excerpts": candidate["relevant_excerpts"],
            "reasoning": candidate["reasoning"]
        }

        top_matches.append(match)

    output = {
        "job_description": job_description,
        "top_matches": top_matches
    }

    return output




def save_results(output, filepath):
    """
    Save job matching results as JSON.
    """

    os.makedirs(
        os.path.dirname(filepath),
        exist_ok=True
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )





def main():

    if len(sys.argv) > 1:
        job_path = sys.argv[1]
    else:
        job_path = "job_descriptions/python_developer.txt"

    print("\nLoading job description...")

    job_description = read_job_description(
        job_path
    )


    required_skills = extract_required_skills(
        job_description
    )

    required_experience = extract_required_experience(
        job_description
    )

    must_have_skills = extract_must_have_skills(
        job_description
    )


    print("\n========== JOB REQUIREMENTS ==========\n")

    print(
        f"Required Skills: {required_skills}"
    )


    print(
        f"Must-Have Skills: {must_have_skills}"
    )

    print(
        f"Required Experience: "
        f"{required_experience} years"
    )


    print("\nConnecting to ChromaDB...")

    collection = load_database()

    print(
        f"Records available: {collection.count()}"
    )

    print("\nPerforming semantic search...")

    results = semantic_search(
        collection,
        job_description,
        top_k=collection.count()
    )


    grouped_candidates = group_results_by_candidate(
        results
    )

    ranked_candidates = rank_candidates(
        grouped_candidates,
        required_skills,
        required_experience,
        must_have_skills
    )

    qualified_candidates = [
        candidate
        for candidate in ranked_candidates
        if candidate["meets_must_have"]
    ]

    rejected_candidates = [
        candidate
        for candidate in ranked_candidates
        if not candidate["meets_must_have"]
    ]


    print(
        "\n========== QUALIFIED CANDIDATES ==========\n"
    )

    for rank, candidate in enumerate(
        qualified_candidates[:10],
        start=1
    ):
        print(f"RANK {rank}")

        print(
            f"Candidate: "
            f"{candidate['candidate_name']}"
        )

        print(
            f"Resume: "
            f"{candidate['resume_path']}"
        )

        print(
            f"Experience: "
            f"{candidate['experience_years']} years"
        )

        print(
            f"Matched Skills: "
            f"{candidate['matched_skills']}"
        )

        print(
            f"Final Match Score: "
            f"{candidate['match_score']}/100"
        )

        print(
            f"Meets Must-Have Requirements: "
            f"{candidate['meets_must_have']}"
        )

        print(
            f"Missing Must-Have Skills: "
            f"{candidate['missing_skills']}"
        )

        print(
            f"Experience Requirement Met: "
            f"{candidate['experience_requirement_met']}"
        )

        print(
            f"Reasoning: "
            f"{candidate['reasoning']}"
        )

        print("Relevant Excerpts:")


    print(
        "\n========== REJECTED CANDIDATES ==========\n"
    )

    for candidate in rejected_candidates:

        print(
            f"Candidate: {candidate['candidate_name']}"
        )

        print(
            f"Score: {candidate['match_score']}/100"
        )

        print(
            f"Missing Skills: "
            f"{candidate['missing_skills']}"
        )

        print(
            f"Experience Requirement Met: "
            f"{candidate['experience_requirement_met']}"
        )

        print("-" * 60)


    final_output = create_output(
        job_description,
        qualified_candidates,
        top_k=10
    )

    job_filename = os.path.basename(job_path)

    job_name = os.path.splitext(job_filename)[0]

    output_path = (
        f"results/{job_name}_results.json"
    )

    save_results(
        final_output,
        output_path
    )


    for excerpt in candidate[
            "relevant_excerpts"
        ]:
            print(f"- {excerpt}")

            print("-" * 60)


    print(
        "\n========== OUTPUT SAVED ==========\n"
    )

    print(
        f"Results saved to: {output_path}"
    )

    print(
        f"Qualified candidates returned: "
        f"{len(final_output['top_matches'])}"
    )




if __name__ == "__main__":
    main()