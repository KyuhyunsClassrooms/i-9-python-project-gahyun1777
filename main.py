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

VOLUME_OF_DISTRIBUTION = 50.0

def find_drug(name):
    for drug in drug_database:
        if drug[0] == name:
            return drug[1], drug[2] 
    return None

def simulate_mec(half_life, mec, initial_val):
    hourly_log = []
    current_val = initial_val
    hour = 0
    
    if current_val < mec:
        hourly_log.append([0, round(current_val, 2), "❌ 효과 없음 (MEC 미달)"])
        return hourly_log, -1
    
    while current_val >= mec:
        hourly_log.append([hour, round(current_val, 2), "🟢 효과 유지"])
        current_val = current_val * (0.5 ** (1 / half_life))
        hour += 1
        
    wear_off_hour = hour
    hourly_log.append([hour, round(current_val, 2), "🔴 효과 소멸"])
        
    return hourly_log, wear_off_hour

def display_result(log_data, wear_off_hour, calc_type, drug_name):
    unit = "mg/L" if calc_type == "농도" else "mg"
    
    print("\n" + "="*50)
    print(f" 시간 |   체내 수치({unit})   |       약효 상태")
    print("="*50)
    
    for row in log_data:
        if row[0] > 24:
            print(" ...  |     (24시간 이후 계산 생략)     |")
            break
        print(f" {row[0]:>2}시  |    {row[1]:>10} {unit:<4} |  {row[2]}")
        
    print("="*50)
    
    if wear_off_hour == -1:
        print(f" [분석 결과] {drug_name}은(는) 초기 복용량이 너무 적어 처음부터 효과가 나타나지 않습니다.")
    else:
        print(f" [분석 결과] {drug_name}이(가) 처음 효과가 소멸되는 시기는 {wear_off_hour}시간 후입니다.")
        
    print("="*50)


if __name__ == "__main__":
    print("=== 체내 잔류 농도 / 용량 계산기 ===")
    
    user_input = input(" 약물 이름과 초기 복용량(mg)을 입력하세요 (예: 타이레놀 500): ").split()
    
    if len(user_input) < 2:
        print(" 입력 형식이 올바르지 않습니다.")
    else:
        drug_name = user_input[0]
        try:
            initial_dose = float(user_input[1])
            calc_type = input("계산 방식을 선택하세요 (농도 / 용량): ")
            
            if calc_type not in ["농도", "용량"]:
                print(" '농도' 또는 '용량' 중 하나를 정확히 입력해야 합니다.")
            else:
                drug_info = find_drug(drug_name)
                
                if drug_info is not None:
                    half_life, mec_concentration = drug_info
                    
                    if calc_type == "농도":
                        initial_val = initial_dose / VOLUME_OF_DISTRIBUTION 
                        target_mec = mec_concentration                      
                    else: 
                        initial_val = initial_dose                          
                        target_mec = mec_concentration * VOLUME_OF_DISTRIBUTION 
                    
                    log, wear_off_hour = simulate_mec(half_life, target_mec, initial_val)
                    
                    display_result(log, wear_off_hour, calc_type, drug_name)
                    
                else:
                    print("❌ 데이터베이스에 없는 약물입니다.")
                    
        except ValueError:
            print("❌ 복용량은 숫자로 입력해야 합니다.")