# AI 활용 자유 주제 파이썬 미니 프로젝트
# 이름 또는 학번: 21002 김가현
# 프로젝트 주제: 반감기에 따른 체내 잔류 농도와 용량 계산기

drug_database = [
    ["타이레놀", 3, 3.0],   
    ["부루펜", 2, 2.0],    
    ["탁센", 14, 3.0],     
    ["지르텍", 8, 0.06],   
    ["아스피린", 3, 6.0]    
]

VOLUME_OF_DISTRIBUTION = 50.0  # 성인 평균 분포 용적 50L

# ==========================================
# 2단계: 핵심 기능 함수
# ==========================================

def find_drug(name):
    # 입력값의 앞뒤 공백을 제거하여 검색 오류 방지
    name = name.strip()
    for drug in drug_database:
        # 대소문자나 공백에 구애받지 않도록 처리
        if drug[0].lower() == name.lower():
            return drug[1], drug[2] # 반감기, 농도MEC 반환
    return None

def simulate_mec(half_life, mec, initial_val):
    hourly_log = []
    current_val = initial_val
    hour = 0
    
    # 시작부터 효과가 없는 경우 예외 처리
    if current_val < mec:
        hourly_log.append([0, round(current_val, 2), "❌ 효과 없음 (MEC 미달)"])
        return hourly_log, -1
    
    # 효과가 유지되는 동안 반복 계산
    while current_val >= mec:
        hourly_log.append([hour, round(current_val, 2), "🟢 효과 유지"])
        current_val = current_val * (0.5 ** (1 / half_life))
        hour += 1
        
    wear_off_hour = hour
    hourly_log.append([hour, round(current_val, 2), "🔴 효과 소멸"])
        
    return hourly_log, wear_off_hour

def display_result(log_data, wear_off_hour, calc_type, drug_name, mec_concentration):
    min_required_dose = mec_concentration * VOLUME_OF_DISTRIBUTION
    unit = "mg/L" if calc_type == "농도" else "mg"
    
    print("\n" + "="*50)
    print(f" 시간 |   체내 수치({unit})   |       약효 상태")
    print("="*50)
    
    # 24시간까지 출력하고 그 이상은 생략
    for row in log_data:
        if row[0] > 24:
            print(" ...  |     (24시간 이후 계산 생략)     |")
            break
        print(f" {row[0]:>2}시  |    {row[1]:>10} {unit:<4} |  {row[2]}")
        
    print("="*50)
    
    if wear_off_hour == -1:
        print(f" ⚠️ [분석 결과] {drug_name}은(는) 현재 복용량이 너무 적어 효과가 나타나지 않습니다.")
        print(f"    이 약물이 효과를 발휘하기 위한 최소 용량은 {min_required_dose:.1f}mg입니다.")
    else:
        print(f" 📊 [분석 결과] {drug_name}이(가) 처음 효과가 소멸되는 시기는 {wear_off_hour}시간 후입니다.")
    print("="*50)

# ==========================================
# 3단계: 메인 프로그램
# ==========================================
if __name__ == "__main__":
    print("=== 🏥 체내 잔류 농도 / 용량 시뮬레이터 ===")
    
    user_input = input("👉 약물 이름과 초기 복용량(mg)을 입력하세요 (예: 타이레놀 500): ").split()
    
    if len(user_input) < 2:
        print("❌ 입력 형식이 올바르지 않습니다. (예: 타이레놀 500)")
    else:
        drug_name = user_input[0]
        try:
            initial_dose = float(user_input[1])
            calc_type = input("👉 계산 방식을 선택하세요 (농도 / 용량): ").strip()
            
            if calc_type not in ["농도", "용량"]:
                print("❌ '농도' 또는 '용량' 중 하나를 정확히 입력해야 합니다.")
            else:
                drug_info = find_drug(drug_name)
                
                # 약물이 없을 경우 동적 추가 로직
                if drug_info is None:
                    choice = input(f"❌ '{drug_name}'은(는) DB에 없습니다. 추가할까요? (Y/N): ").upper().strip()
                    if choice == 'Y':
                        hl = float(input("반감기(시간) 입력: "))
                        if hl <= 0:
                            print("❌ 반감기는 0보다 커야 합니다. 계산을 종료합니다.")
                            exit()
                        mec = float(input("최소 유효 농도(MEC, mg/L) 입력: "))
                        if mec <= 0:
                            print("❌ 최소 유효 농도는 0보다 커야 합니다. 계산을 종료합니다.")
                            exit()
                            
                        drug_database.append([drug_name, hl, mec])
                        drug_info = (hl, mec)
                        print("✅ 신규 약물 등록 완료!")
                    else:
                        print("계산을 종료합니다.")
                        exit()

                # 시뮬레이션 데이터 가공 및 실행
                half_life, mec_concentration = drug_info
                
                if calc_type == "농도":
                    initial_val = initial_dose / VOLUME_OF_DISTRIBUTION
                    target_mec = mec_concentration
                else: 
                    initial_val = initial_dose
                    target_mec = mec_concentration * VOLUME_OF_DISTRIBUTION
                
                log, wear_off_hour = simulate_mec(half_life, target_mec, initial_val)
                display_result(log, wear_off_hour, calc_type, drug_name, mec_concentration)
                    
        except ValueError:
            print("❌ 복용량과 설정값은 올바른 숫자여야 합니다.")