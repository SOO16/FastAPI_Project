from typing import Union
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI()

# 모든 출처 허용
origins = ["*"]

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 전체 조회 + 유저 생성 =====
# User 조회 / 생성에 필요한 기본 info
class UserBase(BaseModel):
    # id: int
    username: str
    email: EmailStr
    age: Union[int, None] = None
    # password: str -> password는 받으면 안돼요
    disabled: bool = False

# DB에 들어갈 User 클래스 -> UserBase 상속
class User(UserBase):
    id: int
    password: str 

# User가 회원가입할 때 넣을 필수 정보들을 할당  
class UserCreate(UserBase):
    password: str 
    

class UserPublic(UserBase):
    id: int


users = [
    {
        "id": 1,    # DB indx
        "username": "david123",  # 필수
        "email": "david@gmail.com", # 필수
        "age": None,    # 선택
        "password": "1q2w3e4r!",    # 필수
        "disabled": False,  # 휴면인지 아닌지?
    },
    {
        "id": 2,
        "username": "sylvie456",
        "email": "sylvie@naver.com",
        "age": 30,
        "password": "asdfqwer1234@",
        "disabled": False,
    },
    {
        "id": 3,
        "username": "nana123",
        "email": "nana@hotmail.com",
        "age": 4,
        "password": "mypassword",
        "disabled": True,
    },
]

last_id = 3

@app.get("/api/v1/users", response_model=list[UserPublic], status_code=status.HTTP_200_OK)
def read_users() -> list[UserPublic]:
    return users

# reference
# {
#     "username": "tommy111",  
#     "email": "tommy@kakao.com", 
#     "password": "1q2w3e4r!"    
# }
@app.post("/api/v1/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> UserPublic:
    global last_id

    user_dict = user.model_dump()   # json을 받기 떄문에 dict로 바꿔줌
    last_id += 1
    user_dict.update({"id": last_id})
    users.append(user_dict)
    return user_dict


