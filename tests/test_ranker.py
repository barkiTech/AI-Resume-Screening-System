from app.models.ranker import Ranker

def test_ranker_runs():
    r = Ranker()
    job = "Looking for Python or Java backend engineer with REST APIs and PostgreSQL on AWS."
    cvs = [
        {"id":"a","text":"Python FastAPI PostgreSQL Docker AWS Jenkins REST services."},
        {"id":"b","text":"React Node CSS."}
    ]
    ranked = r.rank(job, cvs)
    assert len(ranked) == 2
    assert ranked[0]["score"] >= ranked[1]["score"]
