
import json, requests, glob

URL = "http://localhost:8080/diagnose"

def run():
    cases = sorted(glob.glob("api/eval/cases/*.json"))
    if not cases:
        print("No hay casos. Creá archivos en api/eval/cases/*.json")
        return
    for f in cases:
        payload = json.load(open(f))
        try:
            r = requests.post(URL, json=payload, timeout=10)
            ok = r.status_code == 200 and all(k in r.json() for k in ("signals","diagnosis"))
            print(f"{f}: {'OK' if ok else 'FAIL'}")
        except Exception as e:
            print(f"{f}: ERROR {e}")

if __name__ == "__main__":
    run()
