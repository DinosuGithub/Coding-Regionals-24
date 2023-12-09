# Database Schema

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