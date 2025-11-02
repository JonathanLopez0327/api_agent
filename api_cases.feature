# language: es
Feature: Casos de API - BDD

  # Caso feliz con request tal cual.
  Scenario: TC-001 - POST - Happy Path
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 200

  # Se elimina el campo businessSearches.0.expectations.businessCity del body
  Scenario: TC-002 - [BODY] Missing field: businessSearches.0.expectations.businessCity
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Campo en null
  Scenario: TC-003 - [BODY] Set null: businessSearches.0.expectations.businessCity
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": null,
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String vacío
  Scenario: TC-004 - [BODY] Empty string: businessSearches.0.expectations.businessCity
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String demasiado largo
  Scenario: TC-005 - [BODY] Too long string: businessSearches.0.expectations.businessCity
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut CreekXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Tipo incorrecto
  Scenario: TC-006 - [BODY] Wrong type (str->int): businessSearches.0.expectations.businessCity
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": 123,
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Se elimina el campo businessSearches.0.expectations.businessCountry del body
  Scenario: TC-007 - [BODY] Missing field: businessSearches.0.expectations.businessCountry
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Campo en null
  Scenario: TC-008 - [BODY] Set null: businessSearches.0.expectations.businessCountry
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": null,
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String vacío
  Scenario: TC-009 - [BODY] Empty string: businessSearches.0.expectations.businessCountry
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String demasiado largo
  Scenario: TC-010 - [BODY] Too long string: businessSearches.0.expectations.businessCountry
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "USXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Tipo incorrecto
  Scenario: TC-011 - [BODY] Wrong type (str->int): businessSearches.0.expectations.businessCountry
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": 123,
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Se elimina el campo businessSearches.0.expectations.businessName del body
  Scenario: TC-012 - [BODY] Missing field: businessSearches.0.expectations.businessName
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Campo en null
  Scenario: TC-013 - [BODY] Set null: businessSearches.0.expectations.businessName
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": null,
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String vacío
  Scenario: TC-014 - [BODY] Empty string: businessSearches.0.expectations.businessName
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String demasiado largo
  Scenario: TC-015 - [BODY] Too long string: businessSearches.0.expectations.businessName
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software SushiXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Tipo incorrecto
  Scenario: TC-016 - [BODY] Wrong type (str->int): businessSearches.0.expectations.businessName
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": 123,
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Se elimina el campo businessSearches.0.expectations.businessState del body
  Scenario: TC-017 - [BODY] Missing field: businessSearches.0.expectations.businessState
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Campo en null
  Scenario: TC-018 - [BODY] Set null: businessSearches.0.expectations.businessState
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": null,
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String vacío
  Scenario: TC-019 - [BODY] Empty string: businessSearches.0.expectations.businessState
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String demasiado largo
  Scenario: TC-020 - [BODY] Too long string: businessSearches.0.expectations.businessState
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FLXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Tipo incorrecto
  Scenario: TC-021 - [BODY] Wrong type (str->int): businessSearches.0.expectations.businessState
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": 123,
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Se elimina el campo businessSearches.0.expectations.businessStreet del body
  Scenario: TC-022 - [BODY] Missing field: businessSearches.0.expectations.businessStreet
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Campo en null
  Scenario: TC-023 - [BODY] Set null: businessSearches.0.expectations.businessStreet
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": null,
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String vacío
  Scenario: TC-024 - [BODY] Empty string: businessSearches.0.expectations.businessStreet
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String demasiado largo
  Scenario: TC-025 - [BODY] Too long string: businessSearches.0.expectations.businessStreet
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina DrXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Tipo incorrecto
  Scenario: TC-026 - [BODY] Wrong type (str->int): businessSearches.0.expectations.businessStreet
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": 123,
              "businessZip": "33073"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Se elimina el campo businessSearches.0.expectations.businessZip del body
  Scenario: TC-027 - [BODY] Missing field: businessSearches.0.expectations.businessZip
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Campo en null
  Scenario: TC-028 - [BODY] Set null: businessSearches.0.expectations.businessZip
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": null
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String vacío
  Scenario: TC-029 - [BODY] Empty string: businessSearches.0.expectations.businessZip
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": ""
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String demasiado largo
  Scenario: TC-030 - [BODY] Too long string: businessSearches.0.expectations.businessZip
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Tipo incorrecto
  Scenario: TC-031 - [BODY] Wrong type (str->int): businessSearches.0.expectations.businessZip
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": 123
            },
            "name": "Software Sushi"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Se elimina el campo businessSearches.0.name del body
  Scenario: TC-032 - [BODY] Missing field: businessSearches.0.name
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            }
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Campo en null
  Scenario: TC-033 - [BODY] Set null: businessSearches.0.name
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": null
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String vacío
  Scenario: TC-034 - [BODY] Empty string: businessSearches.0.name
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": ""
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # String demasiado largo
  Scenario: TC-035 - [BODY] Too long string: businessSearches.0.name
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": "Software SushiXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400

  # Tipo incorrecto
  Scenario: TC-036 - [BODY] Wrong type (str->int): businessSearches.0.name
    Given preparo una solicitud HTTP
    And los headers son:
      | clave | valor |
      | Authorization | Bearer token |
      | Content-Type | application/json |
    And el payload es:
      """json
      {
        "businessSearches": [
          {
            "expectations": {
              "businessCity": "Coconut Creek",
              "businessCountry": "US",
              "businessName": "Software Sushi",
              "businessState": "FL",
              "businessStreet": "4566 San Mellina Dr",
              "businessZip": "33073"
            },
            "name": 123
          }
        ]
      }
      """
    When envío una solicitud "POST" a "https://api.mi-banco/transacciones/crear"
    Then el código de estado debe ser 400
