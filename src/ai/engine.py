import pickle
import pandas as pd

from models import CompensationRequest


def return_prediction(model_file, db_compensation_request: CompensationRequest, new_value: int) -> int:
    row_to_predict = pd.DataFrame(
        columns=['Grad', 'Sex', 'SalaryRange_encoded', 'AgeRange_encoded', 'Localitate_encoded',
                 'Tip_incalzire_principal_encoded', 'Company_name_encoded', 'NrMembriDeFamilie'])
    # row_to_predict = pd.concat([row_to_predict, pd.DataFrame([{
    #         'Grad': new_value,
    #         'Sex': db_compensation_request.sex,
    #         'SalaryRange_encoded': db_compensation_request.salary_range_encoded,
    #         'AgeRange_encoded': db_compensation_request.age_range_encoded,
    #         'Localitate_encoded': db_compensation_request.locality_encoded,
    #         'Tip_incalzire_principal_encoded': db_compensation_request.main_heating_type_encoded,
    #         'Company_name_encoded': db_compensation_request.company_encoded,
    #         'NrMembriDeFamilie': db_compensation_request.number_of_residents,
    #     },])], ignore_index=True)

    row_to_predict = pd.concat([row_to_predict, pd.DataFrame([{
        'Grad': 4,
        'Sex': 1,
        'SalaryRange_encoded': 4,
        'AgeRange_encoded': 0,
        'Localitate_encoded': 1,
        'Tip_incalzire_principal_encoded': 1,
        'Company_name_encoded': 1,
        'NrMembriDeFamilie': 1,
    }, ])], ignore_index=True)

    with open(f'src/ai/{model_file}', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Make predictions with the loaded model
    new_predictions = loaded_model.predict(row_to_predict)
    return int(new_predictions[0])


data = {'Grad': 4, 'Sex': 1, 'SalaryRange_encoded': 1, 'AgeRange_encoded': 0, 'Localitate_encoded': 1,
        'Tip_incalzire_principal_encoded': 1, 'Company_name_encoded': 1, 'NrMembriDeFamilie': 1}



