# 🧭 SQL & Application Logic (AL) Best Practices and Coding Standards  
**For Microsoft SQL Server**

This guide defines the **standards, patterns, and practices** for writing high-quality, maintainable, and performant **T-SQL** and **Application Logic (AL)** code targeting **MSSQL Server**.  

It is designed to be imported into GitHub Copilot or any AI-assisted workflow to ensure consistent SQL development across teams.

---

## 📘 1. Purpose

The purpose of this document is to:
- Establish consistent **coding style** for SQL and stored procedures.
- Promote **performance-oriented** design and **safe transaction handling**.
- Define clear **naming conventions** for schema, tables, and procedures.
- Align with **Microsoft SQL Server best practices**.

---

## ⚙️ 2. Environment Standards

| Area | Rule |
|------|------|
| **SQL Version** | Target SQL Server 2019+ (or Azure SQL). |
| **ANSI Settings** | Always enable `SET ANSI_NULLS ON` and `SET QUOTED_IDENTIFIER ON`. |
| **Transaction Handling** | Use explicit `BEGIN TRAN`, `COMMIT`, and `ROLLBACK`. |
| **Error Handling** | Use `TRY...CATCH` blocks for controlled error flow. |
| **Security** | Apply least privilege (avoid `sa` and `dbo` ownership). |

---

## 🧩 3. Naming Conventions

| Object Type | Convention | Example |
|--------------|-------------|----------|
| **Database** | lowercase, underscore | `hr_system` |
| **Schema** | lowercase | `sales`, `finance` |
| **Table** | singular noun, PascalCase | `Employee`, `InvoiceDetail` |
| **Column** | camelCase | `firstName`, `invoiceDate` |
| **Primary Key** | `PK_<TableName>` | `PK_Employee` |
| **Foreign Key** | `FK_<Child>_<Parent>` | `FK_Invoice_Employee` |
| **Stored Procedure** | `usp_<Action>_<Entity>` | `usp_Get_EmployeeList` |
| **Function** | `ufn_<Action>_<Entity>` | `ufn_Calc_TaxAmount` |
| **View** | `vw_<Entity>` | `vw_ActiveEmployees` |
| **Index** | `IX_<Table>_<Column>` | `IX_Employee_LastName` |
| **Constraint** | `CK_<Table>_<Column>` | `CK_Employee_Age` |

---

## 🔍 4. Query Design Rules

### ✅ DO
- Use **set-based operations** instead of cursors or loops.
- Use **table aliases** (`E`, `D`) for readability.
- Prefer **JOIN** syntax over subqueries.
- Use **SARGable predicates** (Search ARGument ABLE):
  ```sql
  WHERE FirstName = 'John'  -- good
  WHERE LEFT(FirstName, 4) = 'John'  -- bad
  ```
- Always specify **column names** in `INSERT` statements.

### ❌ AVOID
- Using `SELECT *` — list columns explicitly.  
- Using `NOLOCK` unless absolutely required (can cause dirty reads).  
- Scalar functions inside `SELECT` or `WHERE` — they hurt performance.  
- Implicit data type conversions (always match column types).

---

## ⚡ 5. Indexing & Performance

| Area | Rule |
|------|------|
| **Clustered Index** | Always define one (prefer surrogate key). |
| **Non-Clustered Indexes** | Create on frequent `WHERE`, `JOIN`, and `ORDER BY` columns. |
| **Index Naming** | Use pattern `IX_<Table>_<Column>` |
| **Statistics** | Keep up to date via `AUTO_UPDATE_STATISTICS`. |
| **Execution Plans** | Always validate with `SET STATISTICS IO ON` and `SET STATISTICS TIME ON`. |

---

## 🧠 6. Stored Procedure Guidelines

- Include `SET NOCOUNT ON;` at the start.
- Include full **header comments**:
  ```sql
  /*
      Procedure: usp_Get_EmployeeList
      Description: Returns active employees with department names.
      Author: <Your Name>
      Created: 2025-10-19
      Modified: <Date> - <Reason>
  */
  ```
- Use **parameters** with explicit types and sizes.
- Avoid dynamic SQL unless parameterized.
- Always handle transactions with `TRY...CATCH`.

Example:
```sql
CREATE PROCEDURE usp_Update_EmployeeSalary
    @EmployeeId INT,
    @NewSalary MONEY
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRAN;

        UPDATE Employee
        SET Salary = @NewSalary
        WHERE Id = @EmployeeId;

        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        THROW;
    END CATCH;
END
```

---

## 🔒 7. Security Best Practices

- Avoid `xp_cmdshell`, `OPENROWSET`, and direct OS calls.
- Validate all external inputs.
- Use **schema-level permissions**, not table-level.
- Avoid granting `db_owner` or `sysadmin` roles.

---

## 🧹 8. Maintenance Rules

| Area | Rule |
|------|------|
| **Code Review** | Every SQL change must be peer-reviewed. |
| **Source Control** | Store `.sql` and `.md` files in Git (use folders: `/schema`, `/procedures`, `/functions`). |
| **Deployment** | Use versioned migration scripts. |
| **Monitoring** | Track slow queries using `sys.dm_exec_query_stats`. |

---

## 🧭 9. Code Style Conventions

- Indent with **4 spaces**.  
- Keywords in **UPPERCASE** (e.g., `SELECT`, `WHERE`).  
- Object names in **PascalCase** or **camelCase**.  
- One statement per line.  
- Align joins and conditions for readability.

Example:
```sql
SELECT E.EmployeeId,
       E.FirstName,
       D.DepartmentName
FROM   Employee E
JOIN   Department D ON D.DepartmentId = E.DepartmentId
WHERE  E.Status = 'Active';
```

---

## 📈 10. AI / Copilot Integration Notes

When using **GitHub Copilot** with SQL Server projects:
- Use structured comments (`-- @purpose`, `-- @params`, etc.) to help Copilot suggest relevant completions.
- Keep example queries in `/examples` folder for AI context.
- Add schema definitions to `/schema` to improve Copilot accuracy.
- Avoid ambiguous variable names (e.g., `@x`, `@y`).

---

## 📚 References

- [Microsoft SQL Server Transact-SQL Reference](https://learn.microsoft.com/en-us/sql/t-sql/language-reference)
- [SQL Server Query Performance Tuning Guide](https://learn.microsoft.com/en-us/sql/relational-databases/performance)
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)

---

**File:** `introduction.md`  
**Applies To:** SQL Server 2016 and later  
**Author:** Database Engineering Team  
**Version:** 1.0.0  
**Last Updated:** 2025-10-19





You are a senior SQL Server performance expert.

Analyze the following SQL Server query and performance stats.
Propose specific optimizations (indexes, join changes, or query rewrite)
and explain why each change improves performance.

--- Query ---
SELECT 
    c.City,
    AVG(o.Price * o.Quantity) AS AvgRevenue,
    COUNT(DISTINCT c.CustomerID) AS TotalCustomers
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE o.OrderDate > DATEADD(DAY, -180, GETDATE())
GROUP BY c.City
ORDER BY AvgRevenue DESC;

--- Statistics ---
Logical Reads: 15200
CPU time: 120ms
Elapsed time: 300ms

--- Table Structures ---
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Name NVARCHAR(100),
    City NVARCHAR(100),
    Age INT
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    ProductName NVARCHAR(100),
    Quantity INT,
    Price DECIMAL(10,2),
    OrderDate DATETIME
);

Goal: Reduce runtime and logical reads.
