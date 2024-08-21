# API 명세서

---
[노션 링크](https://transparent-innovation-ab0.notion.site/API-efdb45bc655c4c61a7b9bb32392147ef?pvs=4)

# /test

### POST

테스트 요청과 응답을 받습니다

- 요청
    
    테스트 요청입니다.
    
    - Request Form
        
        ```jsx
        {
            "name": "[사용자 이름]"
        }
        ```
        
- 응답
    
    테스트 응답입니다.
    
    - Response Form
        
        ```jsx
        {
            200,
            {
                "message": "안녕하세요, [사용자 이름]"
            }
        }
        ```
        
- 에러
    - 500
        
        서버 에러입니다.
        
        - Response Form
            
            ```jsx
            {
            	500,
            	{
            		"message": "서버 에러입니다."
            	}
            }
            ```
            

---

# /user?userTag=[사용자 태그]

사용자 정보를 읽거나 씁니다.

### POST

사용자 정보를 생성합니다. 이미 존재할 시 덮어쓰기합니다.

- 요청
    
    사용자 정보를 요청받습니다.
    
    - Request Form
        
        ```jsx
        {
            "userInfo": {
                "department": "[학과/전공]",
                "enterYear": "[학번]",
                "class": "[학년]"
            },
            "courseInfo": {
                "MSC": {
                    "credit": "[현재 이수한 MSC 학점]",
                    //과학 또는 실험
                    "science_experiment": [
                        "[예) 물리1,물리실험1,화학1]"
                    ]
                },
                "elective": {
                    "credit":"[현재 이수한 교양과목 학점]",
                    //기초교양(논사글(법사글), 영어, 전기영)
                    "basic": [
                        "[예) 영어,전공기초영어]"
                    ],
                    //필수교양(드래곤볼)
                    "required": [
                        "[예) 예술과디자인,언어와철학]"
                },
                "onlineClass":{
                    "credit":"[현재 이수한 싸강 학점]"
                }
            }
        }
        ```
        
- 응답
    
    201
    
- 에러
    - 500
        
        서버 오류
        
        - Response Form
            
            ```jsx
            500,
            {
            	"message": "알 수 없는 에러가 발생했습니다."
            }
            ```
            

### GET

사용자 정보를 불러옵니다.

- 요청
    
    없음
    
- 응답
    
    사용자 정보를 전송합니다.
    
    - Response Form
        
        ```jsx
        {
            "userInfo": {
                "department": "[학과/전공]",
                "enterYear": "[학번]",
                "class": "[학년]"
            },
            "courseInfo": {
                "MSC": {
                    "credit": "[현재 이수한 MSC 학점]",
                    //과학 또는 실험
                    "science_experiment": [
                        "[예) 물리1,물리실험1,화학1]"
                    ]
                },
                "elective": {
                    "credit":"[현재 이수한 교양과목 학점]",
                    //기초교양(논사글(법사글), 영어, 전기영)
                    "basic": [
                        "[예) 영어,전공기초영어]"
                    ],
                    //필수교양(드래곤볼)
                    "required": [
                        "[예) 예술과디자인,언어와철학]"
                    ]
                },
                "onlineClass":{
                    "credit":"[현재 이수한 싸강 학점]"
                }
            }
        }
        ```
        
- 에러
    - 404
        
        사용자를 찾을 수 없을 때
        
        - Response Form
            
            ```jsx
            404,
            {
            	"message": "사용자 정보가 존재하지 않습니다."
            }
            ```
            

---

# /classes

과목을 업로드하거나 가져옵니다.

### POST

과목을 업로드합니다.

- 요청
    
    과목을 업로드합니다. 이미 존재할 경우 분반을 추가합니다.
    
    - Request Form
        
        ```jsx
        {
        		//학수번호
            "courseNumber": {
                "name": "[과목명]",
                "classification": "[전공/교양/MSC/etc]",
                //전필 여부 (전필이면 1, 아니면 null)
                //전공기초 또한 필수로 이수해야 하므로 전필로 취급
                "isRequiredMajor" : "[1/null]",
                //주관학과 (교양일 시 null) !주의! 주관학과 복수 가능
                "department": [
        		        "[예)경영학전공,산업·데이터공학전공"]
                ],
                //분반 (없을 시 "00")
                "division": {
        		        //담당 교수 !주의! 담당 교수 복수 가능
                    "professor": [
        		            "[예)김승범1,전홍배]"
                    ],
                    //요일 및 시간 예)수10,목111213
                    "period": [
                        {  
        		                "day": "WED",
                            "start": "10",
                            "end": "10"
                        },
                        {
        		                "day": "THU",
        		                "start": "11",
        		                "end": "13"
                        }
                    ]
                }
            },
            ...
        }
        ```
        
- 응답
    - 201
- 에러
    - 500

### GET

과목을 가져옵니다.

- 요청
    
    사용자 태그
    
    - Request Form
        
        `/classes?userTag=[사용자 태그]`
        
- 응답
    
    사용자 정보에 맞게 과목을 불러옵니다.
    
    - Response Form
        
        ```jsx
        {
        		//전공
            "major": [
        		    //학수번호
                "courseNumber":{
                    "name": "[(전공)과목명]",
                    "isRequiredMajor" : "[1/null]",
                    //분반 (없을 시 "00")
                    "division":{
        		        //담당 교수 !주의! 담당 교수 복수 가능
                    "professor": [
        		            "[예)김승범1,전홍배]"
                    ],
                    //요일 및 시간 예)수10,목111213
                    "period": [
        		            {  
        				            "day": "WED",
                            "start": "10",
                            "end": "10"
                        },
                        {
        		                "day": "THU",
        		                "start": "11",
        		                "end": "13"
                        }
                    ]
                },
                ...
            ],
            //교양
            "elective":[
                [교양 과목들]
            ],
            //msc과목
            "MSC":[
                [MSC 과목들]
            ],
            //그 외 (이미 이수한 과목 또는 타 학과 전공)
            "etc":{
                "major":[
                    [이수한 것으로 예상되는 전공과목들]
                ],
                "otherMajor":[
                    [타 학과 전공]
                ],
                "elective":{
                    "basic":[
                        [이수한 기초교양(논사글,영어,전기영)]
                    ],
                    "required":[
        		            [이수한 필수교양(드래곤볼)]
                    ],
                    "optional":[
                        [이수한 일반교양(교선)]
                    ]
                }
            }
        }
        ```
        
- 에러
    - 404
        
        가져올 과목이 없을 때
        
        - response Form
            
            ```json
            {
            		404,
            		{
            				"massage": "과목을 가져올 수 없습니다."
            		}
            }
            ```
            

---

# /primary?userTag=[사용자 태그]

선택한 과목의 우선순위를 설정합니다.

### POST

우선순위를  설정합니다.

- 요청
    
    우선순위를 설정합니다.
    
    - request Form
        
        ```json
        {
        		"[학수번호]": {
        				"professer": "[교수명]",
        				//우선순위 (높음:1, 낮음:0)
        				"primary": "[1/0]"
        		},
        		...
        }
        ```
        
- 응답
    - 201
- 에러
    - 500

### GET

선택한 과목을 보여줍니다.

- 요청
    
    없음
    
- 응답
    
    사용자가 선택한 과목을 전송합니다.
    
    - response Form
        
        ```json
        {
        		{
        				"professer": "[교수명]",
        				"name": "[과목명]"
        		},
        		...
        }
        ```
        
- 에러
    - 404
        
        선택한 과목을 보여줄 수 없을 때
        
        - response Form
            
            ```json
            404,
            {
            		"massage": "선택한 과목을 보여줄 수 없습니다."
            }
            ```
            

---

# /break?userTag=[사용자 태그]

시간표의 공강을 설정합니다.

### POST

공강을 설정합니다.

- 요청
    
    공강을 설정합니다.
    
    - request Form
        
        ```json
        {
        		//시간표는 1교시(9:00~10:00)부터 14교시(22:00~23:00)까지 존재
        		//공강 시간
        		"period" : [
        				{
        						"day": "WED",
        						"start": "1",
        						"end": "2"
        				},
        				{
        						"day": "WED",
        						"start": "4",
        						"end": "5"
        				},
        				{
        						"day": "FRI",
        						"start": "1",
        						"end": "14"
        				}
        		]
        		"range": {
        				"min": "[최소공강시간]",
        				"max": "[최대공강시간]"
        		}
        }
        ```
        
- 응답
    - 201
- 에러
    - 500

### GET

빈 시간표를 보여줍니다.

- 요청
    
    없음
    
- 응답
    - 200
- 에러
    - 404
        - response Form
            
            ```json
            {
            	404,
            	{
            			"massage": "페이지를 불러올 수 없습니다."
            	}
            }
            ```
            

---

# /makeSchedule?userTag=[사용자 태그]

시간표 생성을 요청합니다.

### GET

- 요청
    
    없음
    
- 응답
    
    생성된 시간표를 보여줍니다.
    
    - Response Form
        
        ```jsx
        {
            "results": [
                {
                    "[학수번호]":{
                        "professor": "[교수 이름]",
                        "period": {
                            "start": "[시작 시간]",
                            "end": "[종료 시간]"
                        }
                    },
                    ...
                },
                ...
            ]
        }
        ```
        
- 에러
    - 404
        
        사용자를 찾을 수 없음
        
        - Response Form
            
            ```jsx
            404,
            {
                "message": "사용자를 찾을 수 없습니다."
            }
            ```
            
    - 406
        
        시간표를 만들기 위한 정보가 부족함(과목을 담지 않았거나…)
        
        - Response Form
            
            ```jsx
            406,
            {
                "message": "시간표를 만들기 위한 정보가 부족합니다.",
                "required": [
                    "[부족한 정보들]",
                    ...
                ]
            }
            ```
            
    - 408
        
        시간 초과
        
        - Response Form
            
            ```jsx
            408,
            {
                "message": "가능한 경우의 수가 너무 많습니다."
            }
            ```
