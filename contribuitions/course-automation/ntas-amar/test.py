#from refextract import extract_references_from_file
from pprint import pprint
from github import Github
import os
"""
def reference_counter():
    path = "../devops-course/attic/2020/contributions-2020/essay/"
    essays = ["applelid-kasperli/KTH_DevOps_Essay.pdf","almajni-rezkalla/IaC_Puppet_vs_Ansible.pdf","asratyan-dautaras-sasig/DevOps_Essay_final.pdf","bratfors/KTH-DevOps-essay.pdf","bwest-cwing/Penetration_Testing-Exploiting_software_to_save_millions_of_dollars_bwest_cwing.pdf"]
#the thrid one gave 12 instead of 11
    ref_counts = []
    for val in essays:
        references_new = []
        essay = path + val
        references = extract_references_from_file(essay)
        for val in references:
            if val["raw_ref"] not in references_new:
                references_new.append(val["raw_ref"])
        ref_counts.append(len(references_new))
    pprint(ref_counts)
    return 0
"""

def test_comment():
  GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
  REPO_FULLNAME = os.getenv("REPO_FULLNAME")
  PR_NUMBER = os.getenv("PR_NUMBER")
  print(REPO_FULLNAME)
  print(f"PR number is {PR_NUMBER}")
  github = Github(GITHUB_TOKEN)
  gitrepo = github.get_repo(REPO_FULLNAME)
  issue = gitrepo.get_issue(1)
  issue.create_comment("hello")
  issue2 = gitrepo.get_issue(int(PR_NUMBER))
  issue2.create_comment("Is it working")

if __name__ == "__main__":
  #Areference_counter()
  print("World")
  test_comment()
  
