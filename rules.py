from datetime import datetime, date

class CountryRules:
    @staticmethod
    def calculate_years(start_date_str, end_date_str):
        start = datetime.strptime(start_date_str, '%Y-%m-%d')
        end = datetime.strptime(end_date_str, '%Y-%m-%d')
        years = end.year - start.year - ((end.month, end.day) < (start.month, start.day))
        return max(0, years)

    @staticmethod
    def calculate_bonus(annual_salary, ic_percent, multiplier_percent, end_date_str):
        exit_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Determine the start of the current Bonus Year (Feb 1st)
        if exit_date.month >= 2:
            bonus_start = date(exit_date.year, 2, 1)
        else:
            bonus_start = date(exit_date.year - 1, 2, 1)
            
        days_in_bonus_year = (exit_date - bonus_start).days + 1
        # Use 365 as standard denominator
        proration_factor = max(0, min(1, days_in_bonus_year / 365))
        
        # Full potential bonus = Salary * IC% * Multiplier%
        full_bonus = annual_salary * (ic_percent / 100) * (multiplier_percent / 100)
        prorated_bonus = full_bonus * proration_factor
        
        return round(prorated_bonus, 2), days_in_bonus_year

    @staticmethod
    def calculate_uk(data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        years = CountryRules.calculate_years(start_date, end_date)
        
        age = int(data.get('age', 0))
        annual_salary = float(data.get('annual_salary', 0))
        
        # 1. Statutory Redundancy Calculation
        actual_weekly_pay = annual_salary / 52
        WEEKLY_CAP = 700.00 # Update as needed
        effective_pay = min(actual_weekly_pay, WEEKLY_CAP)
        effective_years = min(years, 20)

        total_multiplier = 0
        for i in range(effective_years):
            current_age = age - i
            if current_age >= 41: total_multiplier += 1.5
            elif current_age >= 22: total_multiplier += 1.0
            else: total_multiplier += 0.5

        statutory_total = total_multiplier * effective_pay

        # 2. Bonus Proration Calculation
        ic_pc = float(data.get('ic_percent', 0))
        mult_pc = float(data.get('multiplier_percent', 0))
        prorated_bonus, bonus_days = CountryRules.calculate_bonus(annual_salary, ic_pc, mult_pc, end_date)

        return {
            "currency": "GBP",
            "statutory_pay": round(statutory_total, 2),
            "bonus_pay": prorated_bonus,
            "total_package": round(statutory_total + prorated_bonus, 2),
            "years_of_service": years,
            "bonus_days": bonus_days,
            "breakdown": f"Redundancy: £{round(statutory_total, 2)} | Bonus: £{prorated_bonus}"
        }