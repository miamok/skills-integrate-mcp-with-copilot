IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJCeS1za2lsaW5nIHNjcmlwdCB0byBhc2Npc3QgdG9wIG9wZW4gaXNzdWVzIGJ5IHRpdGxlIGtleXdvcmRzLgoKVXNhZ2U6CnB5dGhvbiBzY3JpcHRzL3ByaW9yaXppdGVfaXNzdWVzLnB5IC0tVG9LRU4gPEdIVUJfVE9LRU4+IC0tdG9wIDUKIiIiCmltcG9ydCByZXF1ZXN0cwppbXBvcnQgYXJnZXBhcnNlCmZyb21fYXRhcyA9IFsnc2VjdXJpdHknLCAnY3JpdGljYWwnLCAnYnVnJ10KCmtleV9zY29yZXMgPSB7CiAgICdzZWN1cml0eSc6IDUsCiAgICdjcml0aWNhbCc6IDUsCiAgICdidWcnOiA1LAogICAgJ2Vycm9yJzogMywKICAgICdmaXgnOiAzLAogICAgJ3Vyd2VyJzogNQp9CgoKZGVmIHNjb3Jl_title(title):
    t = title.lower()
    score = 0
    for k, v in key_scores.items():
        if k in t:
            score += v
    # small bonus for longer titles (more specific)
    score += min(len(t.split()), 6) * 0.1
    return score


def fetch_issues(owner, repo, token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers['Authorization'] = f"token {token}"
    params = {"state": "open", "per_page": 100, "page": 1}
    issues = []
    while True:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        page_items = r.json()
        if not page_items:
            break
        issues.extend(page_items)
        if 'next' not in r.links:
            break
        params['page'] += 1
    return issues


def main():
    p = argparse.ArgumentParser(description='Prioritize open issues by title keywords')
    p.add_argument('--token', '-t', help='GitHub token (or set GITHUB_TOKEN)')
    p.add_argument('--owner', default='miamok')
    p.add_argument('--repo', default='skills-integrate-mcp-with-copilot')
    p.add_argument('--top', type=int, default=5)
    args = p.parse_args()

    token = args.token or os.environ.get('GITHUB_TOKEN')

    issues = fetch_issues(args.owner, args.repo, token)
    scored = []
    for it in issues:
        # skip PRs
        if 'pull_request' in it:
            continue
        title = it.get('title', '')
        score = score_title(title)
        scored.append((score, it))

    scored.sort(key=lambda x: x[0], reverse=True)

    print(f"Top {args.top} open issues for {args.owner}/{args.repo}:\n")
    for s, it in scored[:args.top]:
        num = it.get('number')
        title = it.get('title')
        url = it.get('html_url')
        print(f"#{num} ({s:.2f}) - {title}\n  {url}\n")


if __name__ == '__main__':
    main()
