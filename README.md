#
User

## Create User

```
POST /api/users/
```

####

#### Parameters

| Name | Type | Description |
| :---: | :---: | :---: |
| username | String | 해당 유저의 고유한 이름 |
| password | Integer | 비밀번호 |
| nickname | String | 웹페이지에서 사용할 이름 |
| user\_type | String | 계정의 유형 |

#### 계정 유형별

| | **일반 계정** | **FaceBook** | **GooGle** |
| :---: | :---: | :---: | :---: |
| username | email | UID | email |
| password | password | X | X |
| nickname | nickname | name | name |
| user\_type\(Fixed\) | NORMAL | FACEBOOK | GOOGLE |

#### Response

statue\_code : 201 Created

```
{
"token": "token_value",
"user": {
"username": "username",
"nickname": "nickname",
"user_type": "user_type"
}
}
```


