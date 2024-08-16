CREATE TABLE dbo.Empleado 
( 
id INT IDENTITY (1, 1) PRIMARY KEY 
, Nombre VARCHAR(128) NOT NULL 
, Salario MONEY NOT NULL 
 );

INSERT dbo.Empleado (Nombre, Salario) 
VALUES ('Juan Perez', 200000.00),
('Maria Lopez', 300000.00),
('Pedro Ramirez', 400000.00),
('Ana Torres', 500000.00),
('Jose Rodriguez', 600000.00),
('Luisa Martinez', 700000.00),
('Carlos Sanchez', 800000.00),
('Sofia Garcia', 900000.00),
('Jorge Hernandez', 1000000.00),
('Laura Diaz', 1100000.00),
('Ricardo Vargas', 1200000.00),
('Fernanda Jimenez', 1300000.00),
('Roberto Chavez', 1400000.00),
('Gabriela Rios', 1500000.00),
('Oscar Mendoza', 1600000.00),
('Diana Paredes', 1700000.00),
('Raul Reyes', 1800000.00),
('Norma Soto', 1900000.00),
('Hector Nava', 2000000.00),
('Lorena Guzman', 2100000.00),
('Armando Fuentes', 2200000.00),
('Carmen Rosas', 2300000.00),
('Martin Serrano', 2400000.00),
('Veronica Mora', 2500000.00),
('Gerardo Pacheco', 2600000.00),
('Silvia Cervantes', 2700000.00),
('Miguel Peralta', 2800000.00),
('Elena Rangel', 2900000.00),
('Francisco Salgado', 3000000.00),
('Patricia Munguia', 3100000.00),
('Alejandro Mora', 3200000.00),
('Gloria Pacheco', 3300000.00),
('Ramon Serrano', 3400000.00),
('Leticia Mora', 3500000.00),
('Javier Pacheco', 3600000.00),
('Martha Serrano', 3700000.00),
('Ricardo Mora', 3800000.00),
('Fernanda Pacheco', 3900000.00),
('Roberto Serrano', 4000000.00),
('Gabriela Mora', 4100000.00),
('Oscar Pacheco', 4200000.00),
('Diana Serrano', 4300000.00),
('Raul Mora', 4400000.00),
('Norma Pacheco', 4500000.00),
('Hector Serrano', 4600000.00),
('Lorena Mora', 4700000.00),
('Armando Pacheco',48000000.00);

CREATE TABLE [dbo].[DBErrors](
	[ErrorID] [int] IDENTITY(1,1) NOT NULL,
	[UserName] [varchar](100) NULL,
	[ErrorNumber] [int] NULL,
	[ErrorState] [int] NULL,
	[ErrorSeverity] [int] NULL,
	[ErrorLine] [int] NULL,
	[ErrorProcedure] [varchar](max) NULL,
	[ErrorMessage] [varchar](max) NULL,
	[ErrorDateTime] [datetime] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

CREATE PROCEDURE [dbo].[ListarEmpleado]
	@OutResulTCode INT OUTPUT
AS
BEGIN
	SET NOCOUNT ON;
	BEGIN TRY
	
	SET @OutResulTCode=0;

	SELECT @OutResulTCode AS OutResulTCode;  -- Este codigo se agrega solo si hay problemas para obtener este  valor como parametros

	SELECT E.[Id]   -- En interfaces a usuario final no se muestra, ni en apis
		, E.[Nombre]
		, E.[Salario]
	FROM dbo.Empleado E 
	ORDER BY E.Nombre;

	END TRY
	BEGIN CATCH
		INSERT INTO dbo.DBErrors	VALUES (
			SUSER_SNAME(),
			ERROR_NUMBER(),
			ERROR_STATE(),
			ERROR_SEVERITY(),
			ERROR_LINE(),
			ERROR_PROCEDURE(),
			ERROR_MESSAGE(),
			GETDATE()
		);

		SET @OutResulTCode=50005  ;  -- Codigo de error standar del profe para informar de un error capturado en el catch

	END CATCH;

	SET NOCOUNT Off;
END;

