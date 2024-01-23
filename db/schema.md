[Return to Documentation home](/README.md)

# Database Schema

The database used for this application is MongoDB.

## Database: "users"
### Collection: "login"
```
{
  _id: <ObjectId>,
  username: <String>
}
```

### Collection: "challengeData"
```
{
  _id: <ObjectId>,
  user_id: <String>,
  completed: [<Int>],
  scores: {<String>: <Int>}
}
```