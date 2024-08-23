import json

def convert_period(period: list) -> list:
    """
    교시 정보를 변환합니다.

    딕셔너리 형태의 교시 정보를 받아와, 시간표 기준 몇행 몇열인지로 변환하여 반환합니다.

    Args:
        period: 딕셔너리 형텨의 교시 정보를 담은 리스트
            ex) 
            [
                {  
                    "day": "WED",
                    "start": 2,
                    "end": 2
                },
                {  
                    "day": "THU",
                    "start": 2,
                    "end": 3
                }
            ]

    Returns:
        입력 받은 교시 정보를 [행, 열]로 반환한 리스트
        ex)
        [
            [1, 2],
            [1, 3],
            [2, 3]
        ]
    """
    converted_periods = []
    for temp in period:
        day = ["MON", "TUE", "WED", "THU", "FRI"].index(temp["day"])
        for t in range(temp["start"], temp["end"] + 1):
            converted_periods.append([t - 1, day])
    
    return converted_periods
    
def convert_period_temp(period: str) -> list:
    converted_periods = []
    for times in period.split(','):
        day = times[0]
        times = times[1:]
        day = ["월", "화", "수", "목", "금"].index(day)

        start = times[0]
        end = times[-1]

        if times.startswith("10"):
            start = "10"
            if times.endswith("12"):
                end = "12"
        if times.startswith("11"):
            start = "11"
            if times.endswith("12"):
                end = "12"
        if times.startswith("13"):
            start = "13"
        if times.startswith("14"):
            start = "14"
        
        if times.endswith("10"):
            end = "10"
        if times.endswith("11"):
            end = "11"
        if times.endswith("13"):
            end = "13"
        if times.endswith("14"):
            end = "14"
        
        for p in range(int(start), int(end)+1):
            converted_periods.append([p-1, day])

    return converted_periods


def convert_period_v2(period):
    converted_periods = []
    for times in period.split(','):
        form = {}
        day = times[0]
        times = times[1:]
        # day = ["월", "화", "수", "목", "금"].index(day)

        for kor, en in zip(["월", "화", "수", "목", "금"], ["MON", "TUE", "WED", "THU", "FRI"]):
            day = day.replace(kor, en)

        start = times[0]
        end = times[-1]

        if times.startswith("10"):
            start = "10"
            if times.endswith("12"):
                end = "12"
        if times.startswith("11"):
            start = "11"
            if times.endswith("12"):
                end = "12"
        if times.startswith("13"):
            start = "13"
        if times.startswith("14"):
            start = "14"
        
        if times.endswith("10"):
            end = "10"
        if times.endswith("11"):
            end = "11"
        if times.endswith("13"):
            end = "13"
        if times.endswith("14"):
            end = "14"

        form["day"] = day
        form["start"] = int(start)
        form["end"] = int(end)
        form["hour"] = int(end) - int(start) + 1
        
        converted_periods.append(form)

    return converted_periods


def print_schedule(available_times):
    """
    available_times를 보기 좋게 출력합니다.
    """
    for asdf in available_times:
        for asdfasdf in asdf:
            if asdfasdf:
                print("□", end=" ")
                continue
            print("■", end=" ")
        print()
    print("-"*50)


def generate_schedule(subjects: str) -> list:
    """
    시간표를 생성합니다.
    
    dfs 알고리즘을 사용합니다.
    우선 공강 시간을 확보하고, 남는 공간에 우선순위 높음 과목을 배치합니다.(우선순위 높음 과목 중 하나라도 넣을 공간이 없을 시 해당 경우는 배제됩니다.)
    그 다음 남는 공간에 우선순위 낮음 과목을 배치합니다.
    마지막으로 만들어진 조합을 과목 갯수가 많은 순서로 정렬해 반환합니다.
    
    Args:
        subject: 과목 정보를 담은 json 문자열
        ex)
        {
            학수번호: {
                name: "과목이름",
                division:{
                    "분반":{
                        "professor": "교수님",
                        "period": [
                            {  
                                "day": "WED",
                                "start": 2,
                                "end": 2
                            },
                            {
                                    "day": "THU",
                                    "start": 2,
                                    "end": 3
                            }
                        ],    
                    },
                    "분반":{
                        "professor": "교수님",
                        "period": [
                            {  
                                "day": "FRI",
                                "start": 2,
                                "end": 4
                            }
                        ],
                    },
                    ...
                }
                primary: [0/1]
            },
            ...
            "000000": {
                name: "break",
                periods: [
                    [행, 열],
                    ...
                ]
            }
        }

    Returns:
        가능한 조합들을 [[학수번호-분반, ...], ...] 형태로 반환
        과목이 많은 순서대로 정렬해서 반환함
    """
    
    available_times = [
    #    MON   TUE   WED   THU   FRI   
        [True, True, True, True, True], # 1 교시
        [True, True, True, True, True], # 2 교시
        [True, True, True, True, True], # 3 교시
        [True, True, True, True, True], # 4 교시
        [True, True, True, True, True], # 5 교시
        [True, True, True, True, True], # 6 교시
        [True, True, True, True, True], # 7 교시
        [True, True, True, True, True], # 8 교시
        [True, True, True, True, True], # 9 교시
        [True, True, True, True, True], # 10교시
        [True, True, True, True, True], # 11교시
        [True, True, True, True, True], # 12교시
        [True, True, True, True, True], # 13교시
        [True, True, True, True, True], # 14교시
    ]

    primary_subjects = []       # 우선순위 높은 과목
    non_primary_subjects = []   # 우선순위 낮은 과목
    breaks = []                 # 공강

    subjects = json.loads(subjects)
    for subject_code in subjects:
        """
        각 과목을
        [
            "name": "과목 이름",
            "code": "학수번호"
            "division": [
                {
                    "professor": "교수님",
                    "code": 분반,
                    "period": [
                        [1, 0],
                        [1, 1],
                        [2, 1]
                    ],
                }
            ]
        ]
        꼴로 변환하여 각 리스트에 추가함.
        """
        subject = subjects[subject_code]

        if subject["name"]=="break":
            for p in subject["periods"]:
                available_times[p[0]][p[1]] = False
            continue

        subject_form = {
            "code": subject_code,
            "name": subject["name"],
            "division": []
        }
        
        for division in subject["division"]:
            temp = {
                "code": division,
                # "professor": subject["division"][division]["professor"],
                "period": convert_period(subject["division"][division]["period"])
            }
            subject_form["division"].append(temp)
        
        # if subject["name"]=="break":
        #     breaks.append(subject_form)
        #     continue
        
        if subject["primary"]==1:
            primary_subjects.append(subject_form)
            continue
        
        non_primary_subjects.append(subject_form)

    # for break_period in breaks[0]["division"][0]["period"]:
    #     available_times[break_period[0]][break_period[1]] = False
    
    def check(available_times: list, periods: list) -> bool:
        """
        과목이 현재 시간표애 들어갈 수 있는지 체크합니다.

        시간표에 넣을 수 있다면 available_times에 해당 과목을 추가합니다.

        Args:
            available_times: 
            periods: 

        Returns:
            현재 시간표에 해당 과목이 들어갈 수 있는지를 bool 자료형으로 반환
        """
        flag = True
        for period in periods:
            flag = flag and available_times[period[0]][period[1]]
        if flag:
            for period in periods:
                available_times[period[0]][period[1]] = False
            return True
        return False
    
    def dfs(available_times: list, remain_primary_subject_group: list, remain_non_primary_subject_group: list, selected_subjects=[]) -> list:
        """
        가능한 모든 경우의 수를 dfs로 찾아냅니다.
        
        Args:
            available_times: 
            remain_primary_subject_group: 
            remain_non_primary_subject_group: 
            selected_subjects: 현재 경우의 수에서 선택한 과목

        Returns:
            현재 상황에서 가능한 경우와 이전 상황에서 가능했던 경우를 모두 리스트 형태로 반환합니다.
        """
        
        # 인수 복사(원본 훼손 방지를 위해)
        remain_primary_subject_group = remain_primary_subject_group[:]
        remain_non_primary_subject_group = remain_non_primary_subject_group[:]
        selected_subjects = selected_subjects[:]
        available_times = [[t for t in temp] for temp in available_times]
        
        results = []
        
        if remain_primary_subject_group==[]:
            if remain_non_primary_subject_group==[]:
                print(selected_subjects)
                print_schedule(available_times)
                return [selected_subjects]
            
            subject = remain_non_primary_subject_group.pop()
            for division in subject["division"]:
                selected_subjects_cp = selected_subjects[:]
                available_times_cp = [[t for t in temp] for temp in available_times]
                if check(available_times_cp, division["period"]):
                    selected_subjects_cp += [subject["code"] + "-" + division["code"]]
                results += dfs(available_times_cp, remain_primary_subject_group, remain_non_primary_subject_group, selected_subjects_cp)
            return results


        subject = remain_primary_subject_group.pop()
        for division in subject["division"]:
            selected_subjects_cp = selected_subjects[:]
            available_times_cp = [[t for t in temp] for temp in available_times]
            if check(available_times_cp, division["period"]):
                selected_subjects_cp += [subject["code"] + "-" + division["code"]]
                results += dfs(available_times_cp, remain_primary_subject_group, remain_non_primary_subject_group, selected_subjects_cp)


        return results
    
    result = dfs(available_times, primary_subjects, non_primary_subjects)
    temp = []
    hashes = []
    for res in result:
        if str(res) in hashes:
            continue
        temp.append(res)
        hashes.append(str(res))
    result = temp
    result.sort(key=len, reverse=True)
    return result


if __name__=="__main__":
    subjects = """
    {
    "410316": {
        "name": "사운드디자인",
        "division": {
            "01": {
                "professor": "이병렬",
                "period": [
                    {
                        "day": "WED",
                        "start": 2,
                        "end": 4
                    }
                ]
            },
            "02": {
                "professor": "곽은기",
                "period": [
                    {
                        "day": "FRI",
                        "start": 2,
                        "end": 4
                    }
                ]
            }
        },
        "primary": 0
    },

    "410211": {
        "name": "타이포그라피(1)",
        "division": {
            "01": {
                "professor": "박유선2",
                "period": [
                    {
                        "day": "TUE",
                        "start": 2,
                        "end": 4
                    }
                ]
            },
            "02": {
                "professor": "석재원",
                "period": [
                    {
                        "day": "MON",
                        "start": 2,
                        "end": 4
                    }
                ]
            },
            "08": {
                "professor": "석재원",
                "period": [
                    {
                        "day": "FRI",
                        "start": 2,
                        "end": 4
                    }
                ]
            },
            "09": {
                "professor": "박지훈4",
                "period": [
                    {
                        "day": "THU",
                        "start": 2,
                        "end": 4
                    }
                ]
            },
            "10": {
                "professor": "박지훈4",
                "period": [
                    {
                        "day": "THU",
                        "start": 6,
                        "end": 8
                    }
                ]
            },
            "11": {
                "professor": "박지훈4",
                "period": [
                    {
                        "day": "FRI",
                        "start": 2,
                        "end": 4
                    }
                ]
            }
        },
        "primary": 0
    },

    "013312": {
        "name": "자료구조및프로그래밍",
        "division": {
            "03": {
                "professor": "이해영1",
                "period": [
                    {
                        "day": "THU",
                        "start": 2,
                        "end": 3
                    },
                    {
                        "day": "FRI",
                        "start": 2,
                        "end": 3
                    }
                ]
            },
            "04": {
                "professor": "이해영1",
                "period": [
                    {
                        "day": "THU",
                        "start": 6,
                        "end": 7
                    },
                    {
                        "day": "FRI",
                        "start": 6,
                        "end": 7
                    }
                ]
            },
            "05": {
                "professor": "배성일",
                "period": [
                    {
                        "day": "TUE",
                        "start": 2,
                        "end": 3
                    },
                    {
                        "day": "THU",
                        "start": 2,
                        "end": 3
                    }
                ]
            },
            "06": {
                "professor": "배성일",
                "period": [
                    {
                        "day": "TUE",
                        "start": 6,
                        "end": 7
                    },
                    {
                        "day": "THU",
                        "start": 6,
                        "end": 7
                    }
                ]
            }
        },
        "primary": 1
    },

    "012207": {
        "name": "통계학",
        "division": {
            "01": {
                "professor": "김남현",
                "period": [
                    {
                        "day": "MON",
                        "start": 4,
                        "end": 4
                    },
                    {
                        "day": "THU",
                        "start": 2,
                        "end": 3
                    }
                ]
            },
            "02": {
                "professor": "박희석",
                "period": [
                    {
                        "day": "TUE",
                        "start": 7,
                        "end": 9
                    }
                ]
            },
            "03": {
                "professor": "박희석",
                "period": [
                    {
                        "day": "WED",
                        "start": 6,
                        "end": 8
                    }
                ]
            }
        },
        "primary": 1
    },

    "002588": {
        "name": "서양사의이해",
        "division": {
            "07": {
                "professor": "김경현1",
                "period": [
                    {
                        "day": "MON",
                        "start": 11,
                        "end": 13
                    }
                ]
            }
        },
        "primary": 0
    },

    "140623": {
        "name": "파이썬데이터분석",
        "division": {
            "01": {
                "professor": "전홍배",
                "period": [
                    {
                        "day": "TUE",
                        "start": 6,
                        "end": 8
                    }
                ]
            }
        },
        "primary": 0
    },
    
    "000000": {
        "name": "break",
        "division": {
            "01": {
                "professor": "undefined",
                "period": [
                    {
                        "day": "MON",
                        "start": 1,
                        "end": 1
                    },
                    {
                        "day": "TUE",
                        "start": 1,
                        "end": 1
                    },
                    {
                        "day": "WED",
                        "start": 1,
                        "end": 1
                    },
                    {
                        "day": "THU",
                        "start": 1,
                        "end": 1
                    },
                    {
                        "day": "FRI",
                        "start": 6,
                        "end": 14
                    }
                ]
            }
        }
    }
}
    """
    # print(generate_schedule(subjects))

    print(convert_period("월234,화123,수13"))