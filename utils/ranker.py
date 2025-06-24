def rank_resume(matched, job_desc):
    total = len(job_desc.split())
    return min(int((len(matched) / total) * 100), 100)
