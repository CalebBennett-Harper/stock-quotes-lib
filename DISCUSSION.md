# Stock Quotes Library

## Implementation Discussion

### Compromises Due to Time Constraints

- **Limited Error Handling:** Basic error handling implemented; more robust handling required for production (e.g., rate limit handling, retries).
- **Basic Caching:** Simple in-memory caching provided; production would benefit from persistent caching like Redis.
- **Limited Testing:** Comprehensive unit and integration tests not implemented.
- **Documentation:** Inline documentation could be more detailed, especially regarding edge cases.
- **Data Validation:** Basic validation implemented; production usage would require more comprehensive validation.

### Versioning Approach

Use **Semantic Versioning (SemVer)**:

- **Major (X.0.0):** Breaking changes
- **Minor (0.X.0):** New, backward-compatible features
- **Patch (0.0.X):** Backward-compatible bug fixes

Additional strategies include:

- Maintain a `CHANGELOG.md` file.
- Use Git tags for version marking.
- Clearly document API stability.
- Provide clear deprecation policies.

### Publishing the Library

- **Preparation:** Ensure complete `setup.py`, structured package, and documentation (`LICENSE`, `README`).
- **PyPI Publishing:**
  ```bash
  python setup.py sdist bdist_wheel
  twine upload dist/*
  ```
- **Documentation:** Host on Read the Docs or GitHub Pages with installation instructions and API reference.
- **CI/CD:** Set up automated testing and publishing with GitHub Actions or similar tools.
- **Community:** Create contributing guidelines and issue templates.

### Service-Based Design Approach

If designed as a service rather than a library:

- **API Design:**
  - RESTful API with endpoints for each function (lookup, get_min, get_max)
  - OpenAPI/Swagger documentation
  - Authentication and rate limiting

- **Architecture:**
  - Microservice architecture for scalability
  - Separate services for data fetching, caching, and API endpoints
  - Message queue for asynchronous processing

- **Caching Strategy:**
  - Redis or similar for fast in-memory caching
  - Tiered caching with different TTLs based on data freshness
  - Background jobs to pre-fetch popular data

- **Scalability:**
  - Horizontal scaling for API servers
  - Database sharding for large datasets
  - Load balancing across multiple instances

- **Monitoring and Logging:**
  - Comprehensive logging for debugging and auditing
  - Metrics collection for performance monitoring
  - Alerting for service disruptions or API rate limit issues

### Additional Implementation Comments

- **Mock Data Support:** Added mock client implementation for testing without hitting API limits.
- **International Symbol Support:** Library handles international stock symbols (e.g., TSCO.LON).
- **API Key Management:** Flexible approach using environment variables or direct parameter passing.
- **Date Handling:** Robust date string handling with proper DataFrame indexing.
- **Function Design:** Clear, consistent API with intuitive parameter names and return values.

### Time Spent on the Exercise

Approximately 1-2 hours were spent on this exercise, including:
- Initial library design and implementation
- Adding features like caching and international symbol support
- Debugging API key and date handling issues
- Creating example scripts and mock data implementation
- Documentation and code organization

### Feedback on the Exercise

This exercise was well-designed to test a range of skills:

- **API Integration:** Working with external APIs and handling their constraints
- **Data Processing:** Using pandas for efficient data manipulation
- **Error Handling:** Dealing with API limits and unexpected responses
- **Library Design:** Creating a clean, usable API for end users
- **Documentation:** Explaining how to use the library effectively

The Alpha Vantage API rate limit was a realistic constraint that forced thinking about efficient caching and alternative approaches like mock data. The exercise strikes a good balance between being complex enough to demonstrate skills but focused enough to complete in a reasonable time frame.
