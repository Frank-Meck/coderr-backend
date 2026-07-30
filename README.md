# 🚀 Projektname

## Plattform für Kunden und Business User zur Erstellung, Verwaltung und Bestellung von Dienstleistungen

---

# 📌 Übersicht

Dieses Projekt stellt eine REST-API-basierte Plattform bereit, auf der Business User Dienstleistungen als Angebote veröffentlichen und Kunden diese Angebote bestellen und bewerten können.

Das System unterstützt zwei Benutzerrollen:

| Rolle | Funktionen |
|---|---|
| 👤 Customer | Angebote ansehen, Bestellungen erstellen, Business Profile bewerten |
| 🏢 Business User | Angebote erstellen, verwalten und Bestellungen bearbeiten |

---

# 📑 Inhaltsverzeichnis

- [Features](#features)
- [Technologien](#technologien)
- [Architektur](#architektur)
- [Datenmodell](#datenmodell)
- [API Dokumentation](#api-dokumentation)
- [Authentifizierung](#authentifizierung)
- [Berechtigungen](#berechtigungen)
- [Installation](#installation)
- [Entwicklung](#entwicklung)
- [Lizenz](#lizenz)

---

# ✨ Features

## 🔐 Authentication

Funktionen:

- Registrierung neuer Benutzer
- Login mit Token Authentication
- Verwaltung verschiedener Benutzerrollen

Benutzertypen:

```text
customer
business
```

---

# 👤 Profile

Benutzerprofile können:

- abgerufen werden
- aktualisiert werden
- nach Benutzerart gefiltert werden

Funktionen:

- ✅ Eigenes Profil bearbeiten
- ✅ Business Profile anzeigen
- ✅ Customer Profile anzeigen
- ✅ Profilbilder verwalten

---

# 🛒 Angebote (Offers)

Business User können Dienstleistungen als Angebote erstellen und verwalten.

Funktionen:

- ✅ Angebote anzeigen
- ✅ Angebote erstellen
- ✅ Angebote bearbeiten
- ✅ Angebote löschen
- ✅ Angebotsdetails abrufen

Ein Angebot besteht aus mehreren Paketen:

```text
Offer

├── Basic
├── Standard
└── Premium
```

---

# 📦 Bestellungen (Orders)

Customer können Angebote bestellen.

Funktionen:

- ✅ Eigene Bestellungen anzeigen
- ✅ Neue Bestellungen erstellen
- ✅ Bestellstatus ändern
- ✅ Bestellungen verwalten

Mögliche Status:

```text
in_progress
completed
cancelled
```

---

# ⭐ Bewertungen (Reviews)

Kunden können Business User bewerten.

Funktionen:

- ✅ Bewertungen anzeigen
- ✅ Bewertungen erstellen
- ✅ Bewertungen bearbeiten
- ✅ Bewertungen löschen

Regel:

> Ein Kunde darf pro Business Profil nur eine Bewertung erstellen.

---

# 📊 Plattform Statistiken

Endpoint:

```http
GET /api/base-info/
```

Liefert:

- Anzahl Bewertungen
- Durchschnittliche Bewertung
- Anzahl Business Profile
- Anzahl Angebote

---

# 🛠 Technologien

## Backend

- Python
- Django
- Django REST Framework
- REST API
- Token Authentication

## Datenbank

Unterstützt:

- PostgreSQL
- SQLite (Development)

## Frontend

Das Frontend kommuniziert über REST-Endpunkte mit dem Backend.

---

# 🏗 Architektur

```text
┌─────────────┐
│  Frontend   │
└──────┬──────┘
       │
       │ REST API
       │
┌──────▼──────┐
│   Django    │
│  Backend    │
└──────┬──────┘
       │
┌──────▼──────┐
│ Database    │
└─────────────┘
```

---

# 🗄 Datenmodell

## User

| Feld | Beschreibung |
|---|---|
| id | Primärschlüssel |
| username | Benutzername |
| email | E-Mail |
| password_hash | Passwort Hash |
| type | customer/business |
| created_at | Erstellung |

---

## Profile

| Feld | Beschreibung |
|---|---|
| id | Primärschlüssel |
| user_id | Fremdschlüssel User |
| first_name | Vorname |
| last_name | Nachname |
| file | Profilbild |
| location | Standort |
| tel | Telefonnummer |
| description | Beschreibung |
| working_hours | Arbeitszeiten |

Beispiel:

```text
media/profile_pictures/user.jpg
```

Hinweis:

Das Feld `file` speichert normalerweise nur den Pfad zum Bild.

Das eigentliche Bild liegt im Media Storage.

---

## Offer

| Feld | Beschreibung |
|---|---|
| id | Primärschlüssel |
| creator_id | Business User |
| title | Titel |
| image | Angebotsbild |
| description | Beschreibung |
| created_at | Erstellung |
| updated_at | Aktualisierung |

---

## OfferDetail

| Feld | Beschreibung |
|---|---|
| id | Primärschlüssel |
| offer_id | Angebot |
| title | Paketname |
| revisions | Änderungen |
| delivery_time_in_days | Lieferzeit |
| price | Preis |
| features | Funktionen |
| offer_type | Pakettyp |

Beispiele:

```text
basic
standard
premium
```

---

## Order

| Feld | Beschreibung |
|---|---|
| id | Primärschlüssel |
| customer_id | Kunde |
| business_id | Anbieter |
| title | Titel |
| revisions | Änderungen |
| delivery_time_in_days | Lieferzeit |
| price | Preis |
| features | Funktionen |
| offer_type | Pakettyp |
| status | Status |
| created_at | Erstellung |
| updated_at | Aktualisierung |

---

## Review

| Feld | Beschreibung |
|---|---|
| id | Primärschlüssel |
| business_id | Business User |
| reviewer_id | Kunde |
| rating | Bewertung |
| description | Beschreibung |
| created_at | Erstellung |
| updated_at | Aktualisierung |

---

# 🔌 API Dokumentation

Basis URL:

```text
/api/
```

---

# 🔐 Authentication API

## Registrierung

```http
POST /api/registration/
```

Request:

```json
{
  "username": "exampleUsername",
  "email": "example@mail.de",
  "password": "examplePassword",
  "repeated_password": "examplePassword",
  "type": "customer"
}
```

---

## Login

```http
POST /api/login/
```

Request:

```json
{
  "username": "exampleUsername",
  "password": "examplePassword"
}
```

---

# 👤 Profile API

| Methode | Endpoint |
|---|---|
| GET | `/api/profile/{pk}/` |
| PATCH | `/api/profile/{pk}/` |
| GET | `/api/profiles/business/` |
| GET | `/api/profiles/customer/` |

---

# 🛒 Offer API

| Methode | Endpoint |
|---|---|
| GET | `/api/offers/` |
| POST | `/api/offers/` |
| GET | `/api/offers/{id}/` |
| PATCH | `/api/offers/{id}/` |
| DELETE | `/api/offers/{id}/` |
| GET | `/api/offerdetails/{id}/` |

---

# 📦 Order API

| Methode | Endpoint |
|---|---|
| GET | `/api/orders/` |
| POST | `/api/orders/` |
| PATCH | `/api/orders/{id}/` |
| DELETE | `/api/orders/{id}/` |
| GET | `/api/order-count/{business_user_id}/` |
| GET | `/api/completed-order-count/{business_user_id}/` |

---

# ⭐ Review API

| Methode | Endpoint |
|---|---|
| GET | `/api/reviews/` |
| POST | `/api/reviews/` |
| PATCH | `/api/reviews/{id}/` |
| DELETE | `/api/reviews/{id}/` |

---

# 🔑 Authentifizierung

Geschützte Endpoints benötigen einen Token.

Header:

```http
Authorization: Token <token>
```

---

# 🔒 Berechtigungen

## Customer

Darf:

- ✅ Angebote ansehen
- ✅ Bestellungen erstellen
- ✅ Bewertungen erstellen

---

## Business User

Darf:

- ✅ Angebote erstellen
- ✅ Angebote bearbeiten
- ✅ Angebote löschen
- ✅ Bestellungen verwalten

---

## Admin

Darf:

- ✅ Systemverwaltung
- ✅ Bestellungen löschen

---

# ⚙️ Installation

Repository klonen:

```bash
git clone <repository-url>
```

```bash
cd <project-folder>
```

Virtuelle Umgebung erstellen:

```bash
python -m venv venv
```

Aktivieren:

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```
## Umgebungsvariablen konfigurieren

Erstelle eine lokale Konfigurationsdatei auf Basis der Vorlage:

```bash
cp .env.example .env
```

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

Passe anschließend die Werte in der `.env` an, insbesondere:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- Datenbankeinstellungen (`DB_*`)

Migration:

```bash
python manage.py migrate
```

Server starten:

```bash
python manage.py runserver
```

Server:

```text
http://127.0.0.1:8000/
```

---

# 👨‍💻 Entwicklung

Neue Migration:

```bash
python manage.py makemigrations
```

Migration ausführen:

```bash
python manage.py migrate
```

Tests:

```bash
python manage.py test
```

---


# 📄 Lizenz

MIT License