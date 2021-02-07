## Dependencies

1. requests

## To Do

1. Change to namespace packaging
2. Fix the JSONDecodeError, issue with either
   1. REST API
   2. requests.post()
   3. Change request to HTTPS using SSL certificate
   4. ~~json() methods~~
   5. ~~Encoding of data, the response.content property is in binary~~
      1. ~~but the encoding can be converted successfully~~
3. Add a module that checks for existing solutions in a given path, to avoid redownloading all solutions

## Further:

1. Understand REST API
2. Refactoring
3. Add some sort of visual marker showing number of files downloaded and estimated time
