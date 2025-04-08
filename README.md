## Distinctiveness and Complexity

The **Gakusei System** is a Management System for **Enrollments**, **Schedules**, and **Monthly Payments**, designed for a Language Learning Academy, mainly focused on Japanese and English.

### Main Features

#### Student and Sensei (Teachers) Management
- Create and edit Students and Senseis  
- View detailed information for each Student and Sensei  
- Display all Student/Sensei records in a paginated and ordered list  
- Search specific Student/Sensei records using any available field in their respective models  

#### Class Management
- Create and edit Classes  
- View Class details  
- Enroll Students into Classes  
- Manage Class Schedules  
- Track **Class Days** and **Student Attendance**  
- Handle **Payments** and **Payment Status** for each Class and Student  

#### Additional Records
- Register **Branches**, **Courses**, and **Payment Methods** used by the Academy  
- Register which Students have a **Scholarship** or **Special Discount** for Class fees  

### Other Internal Functionalities

- Generate pending payment records for all Active Classes  
- Automatically calculate the tuition fee at the moment of Student enrollment  
- Show or hide Students and Senseis during Class creation/enrollment depending on whether their Status is *Active* or *Retired*  
- Display Branch locations via Google Maps (if a valid link is provided)




## What’s Contained in Each File

### `models.py`

This file contains all the models of the system. Here is a list of all the models:

- **Persona** (Person)  
- **Sensei** (Teachers)  
- **Representante** (Representative)  
- **Estudiante** (Student)  
- **Curso** (Course)  
- **Sede** (Branch)  
- **Clase** (Class)  
- **Horario** (Schedule)  
- **Inscripciones** (Registrations)  
- **Becas** (Scholarships)  
- **Becados** (Scholarship Recipients)  
- **DescuentoEspecial** (Special Discount)  
- **MetodosPagos** (Payment Methods)  
- **Pagos** (Payments)  
- **Solvencias** (Payment Statuses)  
- **Comprobantes** (Receipts)  
- **DiaDeClase** (Class Day)  
- **Asistencias** (Attendance)



### Model Descriptions

#### `Persona`
Base model that contains personal information fields, used as a parent class for `Sensei`, `Representante`, and `Estudiante`.

#### `Sensei`
Inherits from `Persona`. Used to register academic information for teachers. Contains a **Status** field which can be either **Active** or **Retired**. If a `Sensei` is marked as Retired, they cannot be assigned to a Class.

#### `Estudiante`
Inherits from `Persona`. Contains a **Status** field and a foreign key to a `Representante`. Like `Sensei`, if the Student is marked as Retired, they cannot be enrolled in a Class.

#### `Representante`
Also inherits from `Persona`. It has a one-to-many relationship with `Estudiante`. A Representative can be responsible for multiple Students, but each Student only has one Representative.

#### `Curso`
Stores the name of a course, such as "Japanese N5", "English A2", etc. Has a one-to-many relationship with `Clase`.

#### `Sede`
Stores the location data, contact methods, and even a Google Maps link for each academy branch. It has a one-to-many relationship with `Clase`.

#### `Clase`
Registers the Course being taught, its Branch, assigned Sensei, start date, price, and class status.  
Optionally, an end date can be specified.

The **Status** field has four possible values:
- **Active**
- **Paused**
- **Suspended**
- **Finished**

Classes marked as **Suspended** or **Finished** cannot receive new Student enrollments or generate new pending payments.

#### `Horario`
Registers the weekday, start time, and end time of a Class schedule. Has a many-to-one relationship with `Clase`.

#### `Becas`
Stores the scholarships provided by the academy.  
A Scholarship record contains:
- Name of the scholarship  
- Discount amount  
- Discount type (percentage or fixed amount)  
- Status (Active or Disabled)  

If a Scholarship is marked as **Disabled**, it cannot be assigned to a Student.

#### `Becados`
Tracks which Students have been assigned a Scholarship, and includes an optional observation field.

#### `DescuentoEspecial`
Used to assign a personalized Discount to a specific Student. This Discount is always of fixed amount.

#### `Inscripciones`
Registers a Student's enrollment in a Class, along with their monthly payment amount.  
Payment amount is calculated as follows:

- **If the Scholarship is Fixed**:  
  `(Class Price - Special Discount) - Scholarship`

- **If the Scholarship is Percentage-based**:  
  `((Class Price - Special Discount) * Scholarship) / 100`

This amount can be manually adjusted at the time of enrollment.

#### `MetodosPagos`
Registers all Payment Methods used by the academy.

#### `Pagos`
Stores Payment information for a Student’s monthly tuition in a specific Class.  
It includes:
- Student who made the payment  
- Class paid for  
- Payment method  
- Amount paid  
- Transaction reference  
- Payment date  
- System registration date  
- An optional observation  

Upon saving a payment, related `Solvencias` and `Comprobantes` are automatically calculated and generated.

#### `Solvencias`
Tracks the monthly payment status of a Student for a specific Class.  
Statuses include:
- **Pagada** (Paid)
- **Abonada** (Partially Paid)
- **Sin Pagar** (Unpaid)

#### `Comprobantes`
Tracks how much was paid toward each individual `Solvencia`, based on a `Pago`.

#### `DiaDeClase`
Stores information about a Class Day on a specific date, including:
- Schedule used  
- Class number  
- Date  
- Status (Held, Suspended, Cancelled)  
- Optional observation  

#### `Asistencias`
Tracks whether a Student attended a specific `DiaDeClase`.

---

### `views.py`

The model views are mostly defined using Django’s *class-based views*. Additionally, they are grouped according to the Model they interact with, and at the beginning of each section, is defined the route of each model templates folder.

In `settings.py`, is set the middleware **LoginRequiredMiddleware** in order to made necessary the use of the login page. For that reason, the views `login_view` and `logout_view` have the `login_not_required` decorator.

This file also contains several internal APIs used by the system. Some of their functionalities include:

- Retrieving records of Students, Senseis Classes and Payment Statuses
- Generating styled formsets (with Cristy Forms) on the back-end
- Automatically generating pending Payment Statuses for active Classes

Lastly, this file includes the login and logout views, as well as the `paginator_filter_view()` function, which is responsible for generating **search filters** and **paginating results** for a specific Model and its corresponding ModelFilter.

---

### `signals.py`

This file handles the creation of a special **fallback Sensei** entry, used when a **Sensei** assigned to a **Class** is deleted.

This fallback Sensei is not normally visible and its detail page can only be accessed in two ways:
- Through the link found on the detail page of a Class whose Sensei has been deleted
- By directly entering the fallback Sensei's `id` into the browser's search bar

When a migration is performed or a `Sensei` assigned to a Class is deleted, the system checks whether the fallback Sensei is already registered:
- If it **does not exist**, it is created automatically  
- If it **already exists**, the operation continues normally without changes

---

### `forms.py`

This file defines several of the forms used by the system's class-based views and APIs. However, most models use the forms automatically generated by Django’s class-based views.

The forms for `Sensei`, `Estudiante`, and `Representante` inherit from the `BasePersona` mixin, which provides the personal data fields and their ordering. These forms also override the `__init__` and `save` methods to ensure the model data is loaded and saved correctly.

Other forms in this file are used to generate *formsets* or are used directly by the system’s APIs.

---

### `filters.py`

This file contains the functions that define the **search filter forms** for each Model. These filters are used with the **Django Filters** library.

---


### `solvencias_generator.py`

This file defines the function used to **generate the pending Payment Statuses (`Solvencias`)** for each student registered in a Class. 

The function works as follows:
1. All `Clase` objects with status **Active** are retrieved  
2. The function loops through each `Clase`  
3. All `Inscripciones` (Registrations) for that Class are obtained  
4. The **start date** of the Class and the **current date** are compared to calculate the **number of months** between them  
5. A second loop runs through each Registration in the Class  
6. For **each month** between the Class start date and the current date, the system uses `get_or_create()` to create or retrieve a `Solvencia`:
   - If a `Solvencia` already exists, nothing happens  
   - If it does **not** exist, a new `Solvencia` is created with **status: pending** for that specific month  
7. Finally, the function returns:
   - A **completion message**, and  
   - A **boolean value** indicating whether the process was successful or not


---

### `Templates/ Layouts`

Each Model has its own folder, which usually contains the following files: `list.html`, `create.html`, `edit.html`, `detail.html`, `delete.html`, and `filter.html`.

These files **extend** their respective layout templates: `list-layout.html`, `create-layout.html`, `edit-layout.html`, `detail-layout.html`, `delete-layout.html`, and `filter-layout.html`.  
All of these layout templates, in turn, **extend from** the base layout: `layout.html`.

Additionally:
- `login.html` is used for the **login screen**
- `index.html` is used for the **main dashboard** of the system

---

### `Static/`

This folder contains:
- The **JavaScript files** for each page of the system  
- The **background image**
- All the required files from the following libraries:
  - **Bootstrap**
  - **jQuery**
  - **Select2**
  - **Select2 Bootstrap Theme**



## How to Run the Application

To start the system, open the terminal and run the following command:

```bash
python manage.py runserver
```

Once the server is running, opening the web page will prompt you to enter a **username** and **password**.

### Default login credentials:

**Admin user:**
- Username: `admin`
- Password: `admin`

**Regular user:**
- Username: `Kita`
- Password: `Kita`

After logging in, you will be able to access the system normally.

> It is recommended to log in using the **Admin** user for full access to the system.



## Any Other Additional Information the Staff Should Know About Your Project

The project is designed in **Spanish**, as it was developed for a **local Language Learning Academy**.

### External libraries used in the project:

- **Python Dateutil** (v2.9.0): used for date calculations  
- **Font Awesome Free** (v6.6.0): used for system icons  
- **Crispy Forms** (Bootstrap 5, 2024.10): used to style the forms  
- **Django Filter** (v25.1): used to filter and search through records
