Alright, here are your documents, each in a separate Markdown file. You can copy the content and save each one as a `.md` file to download them.

-----

# Work Schedule Management

This document describes the system's flow responsible for **Work Schedule Management**, where operational managers daily record the start and end times of shifts, as well as reasons for absence.

## System Flow

1.  **Courier Registration and Maintenance:**

      * The system allows operational managers to register new couriers, entering information such as name, contact details, and unique identifiers.
      * Courier profile information is kept up-to-date, including active status.

2.  **Daily Shift Registration:**

      * For each courier, operational managers daily record the **start and end times of the work shift**.
      * The system can offer intuitive interfaces, such as interactive calendars, to facilitate bulk or individual registration.
      * The system may also allow for the registration of multiple shifts on the same day, if applicable.

3.  **Lunch/Break Management:**

      * The system allows for the configuration of fixed lunch times or mandatory breaks that are automatically deducted from the total shift.
      * Managers may have the flexibility to adjust these times in exceptional cases.

4.  **Absence Reason Registration:**

      * When a courier is absent (sick leave, vacation, unexcused absences, etc.), managers record the **start and end dates of the absence**, along with the **specific reason**.
      * The system can have a predefined list of absence reasons for standardization.
      * Absence information can be flagged as future (for planning) or past (for historical record).

5.  **Data Validation and Consistency:**

      * The system performs validations to ensure data consistency, such as:
          * Verifying that the shift end time is after the start time.
          * Alerting about overlapping shifts or absences.
          * Ensuring all mandatory fields are filled.

6.  **Schedule Data Availability:**

      * Work schedules, including shifts and absences, are stored and made available to other system modules, such as **Offer Management** and **Offer Correction**.
      * This can be done through APIs or data services, ensuring that courier availability is always as accurate as possible.

7.  **Report and Analytics Generation:**

      * The system allows for the generation of reports on workforce utilization, absence rates, hours worked per courier, etc.
      * These reports assist managers in decision-making and operational planning.

## Database Tables

For the Work Schedule Management stage, the database tables are primarily responsible for storing and maintaining operational information:

  * **`ESC_MOTOCICLISTAS`**: A master table for courier data, with `MOTOCICLISTA_ID` (Courier ID), `NOME_MOTOCICLISTA` (Courier Name), `CPF`, `TELEFONE` (Phone), `STATUS_ATIVO` (Active Status).
  * **`ESC_JORNADAS_DIARIAS`**: This would record daily work shifts, with `JORNADA_ID` (Shift ID), `MOTOCICLISTA_ID`, `DATA_JORNADA` (Shift Date), `HORA_INICIO` (Start Time), `HORA_FIM` (End Time), `OBSERVACOES` (Notes).
  * **`ESC_AUSENCIAS`**: This would store courier absences, including `AUSENCIA_ID` (Absence ID), `MOTOCICLISTA_ID`, `DATA_INICIO` (Start Date), `DATA_FIM` (End Date), `TIPO_AUSENCIA_ID` (Absence Type ID), `MOTIVO_DETALHADO` (Detailed Reason).
  * **`ESC_TIPOS_AUSENCIA`**: A supporting table to standardize absence types, with `TIPO_AUSENCIA_ID` (Absence Type ID), `DESCRICAO_TIPO_AUSENCIA` (Absence Type Description, e.g., "Vacation", "Medical Leave", "Unexcused Absence").

## API Endpoints

Work Schedule Management uses APIs for operational managers to register and query information, and also to make data available to other modules.

  * **`POST https://api.yourcompany.com.br/schedule/couriers`**: Registers a new courier.
      * **Example Request**:
        ```json
        {
            "name": "João Silva",
            "cpf": "123.456.789-00",
            "phone": "5521987654321",
            "email": "joao.silva@empresa.com"
        }
        ```
  * **`PUT https://api.yourcompany.com.br/schedule/couriers/{courier_id}`**: Updates information for an existing courier.
      * **Example Request**:
        ```json
        {
            "phone": "5521998765432"
        }
        ```
  * **`POST https://api.yourcompany.com.br/schedule/shifts`**: Registers a courier's daily work shift.
      * **Example Request**:
        ```json
        {
            "courier_id": "MOTO123",
            "shift_date": "2025-06-25",
            "start_time": "06:00",
            "end_time": "18:00",
            "lunch_start_time": "12:00",
            "lunch_end_time": "13:00"
        }
        ```
  * **`PUT https://api.yourcompany.com.br/schedule/shifts/{shift_id}`**: Updates an existing work shift.
      * **Example Request**:
        ```json
        {
            "end_time": "17:30"
        }
        ```
  * **`POST https://api.yourcompany.com.br/schedule/absences`**: Registers an absence for a courier.
      * **Example Request**:
        ```json
        {
            "courier_id": "MOTO123",
            "start_date": "2025-07-01",
            "end_date": "2025-07-05",
            "absence_type_id": 1, // Ex: 1 for "Vacation"
            "detailed_reason": "Scheduled vacation"
        }
        ```
  * **`PUT https://api.yourcompany.com.br/schedule/absences/{absence_id}`**: Updates an existing absence (e.g., change in return date).
      * **Example Request**:
        ```json
        {
            "end_date": "2025-07-07"
        }
        ```
  * **`GET https://api.yourcompany.com.br/schedule/shifts/{courier_id}/{date}`**: Queries a courier's shift on a specific date.
      * **Example Response**:
        ```json
        {
            "courier_id": "MOTO123",
            "shift_date": "2025-06-25",
            "start_time": "06:00",
            "end_time": "18:00",
            "lunch_start_time": "12:00",
            "lunch_end_time": "13:00"
        }
        ```
  * **`GET https://api.yourcompany.com.br/schedule/absences/{courier_id}`**: Queries a courier's future and past absences.
      * **Example Response**:
        ```json
        [
            {
                "absence_id": "A_001",
                "courier_id": "MOTO123",
                "start_date": "2025-07-01",
                "end_date": "2025-07-05",
                "absence_type": "Vacation",
                "detailed_reason": "Scheduled vacation"
            }
        ]
        ```