# Offer Management

This document describes the system's flow responsible for **Offer Management**, which reads courier availability and generates the half-hour time slots to be displayed in the app for clients.

## System Flow

1.  **Reading Work Schedules:**

      * The system begins by accessing updated information from the **Courier Work Schedule Management**.
      * For each courier and each day, the system reads the start and end times of their shift, as well as lunch breaks (e.g., 12:00 PM to 1:00 PM).

2.  **Calculating Daily Availability:**

      * For each courier, the system calculates their effective daily availability by subtracting lunch breaks and any other predefined pauses from the total shift.
      * For example, if a courier works from 06:00 AM to 06:00 PM with a 1-hour lunch break from 12:00 PM to 1:00 PM, their availability will be divided into two blocks: 06:00 AM - 12:00 PM and 1:00 PM - 06:00 PM.

3.  **Generating Time Slots per Courier:**

      * Based on each courier's daily availability, the system generates half-hour intervals.
      * For example, for the courier in the previous example, the slots would be: 06:30 AM, 07:00 AM, 07:30 AM, ..., 11:30 AM, 01:30 PM, 02:00 PM, ..., 05:30 PM.
      * Slots are always generated 30 minutes in advance of the courier's work block start time so that the system can offer the times correctly (e.g., if a shift starts at 06:00 AM, the first offer slot is 06:30 AM).

4.  **Aggregating Offer by Time Slot:**

      * The system aggregates the availability of all couriers for each half-hour interval on each day.
      * This results in a consolidated view of the number of couriers available for each time slot across the entire operation.

5.  **Applying Filters and Business Rules:**

      * Additional business rules are applied, such as maximum offer limits per slot to avoid overloading a single courier or region.
      * Geographic filters can be applied to ensure the offer is relevant to the client's location in the app.
      * The system also considers cities with the highest purchasing potential, as determined by **Demand Forecasting**, prioritizing the offer in those areas.

6.  **Making Offer Available to the App:**

      * The final offer, with half-hour intervals and courier availability, is made available to the client's app.
      * This is typically done via an API, allowing the app to dynamically query and display available times.
      * The offer is generated for the next 30 days, ensuring clients can schedule deliveries in advance.

## Database Tables

For the Offer Management stage, the database tables that feed and store the generated information are:

  * **`OFR_ESCALA_MOTOCICLISTAS`**: Essential for offer management, this would contain daily schedule data, such as `MOTOCICLISTA_ID` (Courier ID), `DATA` (Date), `HORA_INICIO_JORNADA` (Shift Start Time), `HORA_FIM_JORNADA` (Shift End Time), `HORA_INICIO_ALMOCO` (Lunch Start Time), `HORA_FIM_ALMOCO` (Lunch End Time).
  * **`OFR_SLOTS_OFERTADOS`**: This table would contain the time slots actually offered in the app, with `DATA_OFERTA` (Offer Date), `HORARIO_INICIO_SLOT` (Slot Start Time), `HORARIO_FIM_SLOT` (Slot End Time), `CIDADE_ID` (City ID), `QTD_MOTOCICLISTAS_DISPONIVEIS` (Number of Available Couriers).

## API Endpoints

This stage is crucial for the interface with the client's app, so the availability of time slots is provided via API endpoints.

  * **`GET https://api.yourcompany.com.br/offer/available-slots`**: Allows the client's app to query available courier time slots for a given city and date.
      * **Parameters**: `city_id` (required), `date` (optional, default: today + 30 days ahead).
      * **Example Response**:
        ```json
        [
            {
                "date": "2025-07-01",
                "start_time": "06:30",
                "end_time": "07:00",
                "available": true,
                "estimated_couriers": 5
            },
            {
                "date": "2025-07-01",
                "start_time": "07:00",
                "end_time": "07:30",
                "available": true,
                "estimated_couriers": 7
            },
            {
                "date": "2025-07-01",
                "start_time": "12:00",
                "end_time": "12:30",
                "available": false,
                "estimated_couriers": 0
            }
        ]
        ```
  * **`GET https://api.yourcompany.com.br/offer/cities-with-offer`**: Returns a list of cities where courier service is available.
      * **Example Response**:
        ```json
        [
            {"city_id": "SP", "city_name": "São Paulo"},
            {"city_id": "RJ", "city_name": "Rio de Janeiro"}
        ]
        ```

