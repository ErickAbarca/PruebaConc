CREATE PROCEDURE [dbo].[InsertarEmpleado]
    @Nombre VARCHAR(128)
    , @Salario MONEY
    , @OutResulTCode INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY

    SET @OutResulTCode=0;

    SELECT @OutResulTCode AS OutResulTCode;  -- Este codigo se agrega solo si hay problemas para obtener este  valor como parametros

    IF EXISTS (SELECT 1 FROM dbo.Empleado WHERE Nombre = @Nombre)

    BEGIN
        SET @OutResulTCode=50001; 
    END

    ELSE
    BEGIN
        BEGIN TRANSACTION;
        BEGIN
            INSERT INTO dbo.Empleado (Nombre, Salario) VALUES (@Nombre, @Salario);
            COMMIT TRANSACTION;
        END
        BEGIN
            SET @OutResulTCode=0;
        END
    END

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