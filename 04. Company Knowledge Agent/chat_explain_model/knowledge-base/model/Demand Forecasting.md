# Demand Forecasting

This document outlines the system's flow responsible for **Demand Forecasting**, utilizing a SARIMA model to identify cities with the highest purchasing potential and, consequently, direct the scheduling of service slots.

## System Flow

1.  **Historical Data Collection:**

      * The system begins by collecting historical sales and demand data for service slots across different cities.
      * This includes data such as order volume, peak hours, seasonality, and other relevant indicators.
      * This data is extracted from the company's internal databases, ensuring the integrity and consistency of information.

2.  **Holiday Database Loading:**

      * The operational team registers and maintains an updated database with all relevant national, state, and municipal holidays for the company's operating cities.
      * The system loads this holiday database, which will be used as an exogenous variable in the SARIMA model to capture the impact of these events on demand.

3.  **SARIMA Model Execution:**

      * With historical data and the holiday database loaded, the system executes a **SARIMA (Seasonal Autoregressive Integrated Moving Average)** time series forecasting model.
      * The model is adjusted for each city, considering its specific demand characteristics.
      * SARIMA accounts for seasonality, trends, and autoregressive and moving average components to generate accurate forecasts.

4.  **Demand Forecast Generation:**

      * The SARIMA model generates demand forecasts for future periods, focusing on the next 30 days, aligning with the offer horizon.
      * Forecasts are detailed by city and time slot, allowing for granular analysis of purchasing potential.

5.  **City Ranking by Potential:**

      * Based on demand forecasts, the system ranks cities by their purchasing potential.
      * Cities with higher demand forecasts are considered priorities for directing the allocation of service slots.

6.  **Forecast Availability:**

      * Demand forecasts and city rankings are made available to other system modules (such as Offer Management) and to the planning and operations teams.
      * This can be done through APIs, automated reports, or dashboards, ensuring information is accessible for decision-making.

## Database Tables

For the Demand Forecasting stage, the primary database tables involved in information extraction are:

  * **`DMD_HISTORICO_VENDAS`**: This table would store all historical sales and demand data, with columns for `DATA` (Date), `HORA` (Time), `CIDADE_ID` (City ID), `VOLUME_PEDIDOS` (Order Volume), etc.
  * **`DMD_BASE_FERIADOS`**: This would hold the registered holiday database, with `DATA_FERIADO` (Holiday Date), `NOME_FERIADO` (Holiday Name), `CIDADE_ID` (City ID, if it's a municipal/state holiday).

## API Endpoints

While Demand Forecasting is primarily an internal process, the results can be exposed via API for consumption by other internal systems or dashboards.

  * **`GET https://api.yourcompany.com.br/demand/forecasts/cities`**: Returns the ranking of cities by purchasing potential, based on the latest forecasts.
      * **Example Response**:
        ```json
        [
            {
                "city_id": "SP",
                "city_name": "São Paulo",
                "purchase_potential": 95,
                "forecast_next_30_days": 15000
            },
            {
                "city_id": "RJ",
                "city_name": "Rio de Janeiro",
                "purchase_potential": 88,
                "forecast_next_30_days": 12000
            }
        ]
        ```
  * **`GET https://api.yourcompany.com.br/demand/forecasts/cities/{city_id}`**: Provides detailed demand forecasts for a specific city by time slot.
      * **Example Response**:
        ```json
        {
            "city_id": "SP",
            "city_name": "São Paulo",
            "hourly_forecasts": [
                {"date": "2025-07-01", "time": "08:00", "predicted_demand": 250},
                {"date": "2025-07-01", "time": "08:30", "predicted_demand": 270}
            ]
        }
        ```
