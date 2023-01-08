def preprocessing_filter_spec(endpoints):
    filtered = []
    skip = ["/api-docs/", "/healthcheck/", "/static/", "admin"]
    for (path, path_regex, method, callback) in endpoints:
        # Remove all but DRF API endpoints
        if any([s in path for s in skip]):
            continue
        filtered.append((path, path_regex, method, callback))
    return filtered
