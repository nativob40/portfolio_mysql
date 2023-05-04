
## Creacion de la red  para los contenedores

        docker network create app-sqls-plotly



## Inserción y ejecución de la imagen de contenedor de SQL Server para Linux

1. Extraiga la imagen de contenedor de Linux de SQL Server 2022 (16.x) desde Microsoft Container Registry.

        sudo docker pull mcr.microsoft.com/mssql/server:2022-latest


2. Para ejecutar la imagen de contenedor de Linux con Docker, puede usar el siguiente comando desde un shell de Bash

        sudo docker run --network app-sqls-plotly --network-alias sql1 \
        -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<YourStrong@Passw0rd>" \
        -p 1433:1433 --name sql1 --hostname sql1 \
        -d mcr.microsoft.com/mssql/server:2022-latest


En la tabla siguiente, se proporciona una descripción de los parámetros del ejemplo de docker run anterior:

<table>

<tr>
  <td><strong>Parámetro</strong></td>
  <td><strong>Descripción</strong></td>
</tr>

<tr>
  <td>-e "ACCEPT_EULA=Y"</td>
  <td>Establezca la variable ACCEPT_EULA en cualquier valor para confirmar que acepta el Contrato de licencia de usuario final. Configuración requerida para la imagen de SQL Server.</td>
</tr>

<tr>
  <td>-e "MSSQL_SA_PASSWORD=<̣YourStrong@Passw0rd>"</td>
  <td>Especifique su propia contraseña segura con al menos ocho caracteres y que cumpla los requisitos de contraseña de SQL Server. Configuración requerida para la imagen de SQL Server.</td>
</tr>

<tr>
  <td>-e "MSSQL_COLLATION=<̣SQL_Server_collation>"</td>
  <td>Especifique una intercalación de SQL Server personalizada, en lugar de la predeterminadaSQL_Latin1_General_CP1_CI_AS.</td>
</tr>

<tr>
  <td>-p 1433:1433 <̣SQL_Server_collation></td>
  <td>
  Especifique una intercalación de SQL Server personalizada, en lugar de la         predeterminadaSQL_Latin1_General_CP1_CI_AS. Asigne un puerto TCP en el entorno de host (el primer valor) a un puerto TCP en el contenedor (el segundo valor). En este ejemplo, SQL Server escucha en TCP 1433 en el contenedor y este puerto del contenedor se expone al puerto TCP 1433 del host.</td>
</tr>

<tr>
  <td> --name sql1 </td>
  <td>
	Especifique un nombre personalizado para el contenedor en lugar de uno generado aleatoriamente. Si ejecuta más de un contenedor, no podrá usar el mismo nombre.</td>
</tr>

<tr>
  <td> --hostname sql1 </td>
  <td>
  	Se usa para establecer explícitamente el nombre de host del contenedor. Si no especifica el nombre de host, se adopta como predeterminado el identificador del contenedor, que es un GUID del sistema generado aleatoriamente.</td>
</tr>

<tr>
  <td> -d </td>
  <td>Ejecute el contenedor en segundo plano (demonio).</td>
</tr>

<tr>
  <td> mcr.microsoft.com/mssql/server:2022-latest </td>
  <td> La imagen de contenedor de SQL Server para Linux.</td>
</tr>

</table>


3. Para ver los contenedores de Docker, use el comando docker ps.



        docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Status}}\t{{.Networks}}"

    Debería ver una salida similar a esta:

        CONTAINER ID   NAMES   PORTS                                       STATUS      NETWORKS
        eefc3bf6f53a   sql1    0.0.0.0:1433->1433/tcp, :::1433->1433/tcp   Up 8 days   red_prueba


## Cambio de la contraseña de administrador del sistema
La cuenta SA es un administrador del sistema en la instancia de SQL Server que se crea durante la instalación. Después de crear el contenedor de SQL Server, la variable de entorno MSSQL_SA_PASSWORD especificada se reconoce mediante la ejecución de echo $MSSQL_SA_PASSWORD en el contenedor. Por motivos de seguridad, cambie la contraseña de administrador del sistema.

Elija una contraseña segura que se usará para el usuario SA.

Use docker exec para ejecutar sqlcmd a fin de cambiar la contraseña mediante Transact-SQL. En el ejemplo siguiente, la contraseña anterior y la nueva se leen de la entrada del usuario.

        sudo docker exec -it sql1 /opt/mssql-tools/bin/sqlcmd \
        -S localhost -U SA \
        -P "$(read -sp "Enter current SA password: "; echo "${REPLY}")" \
        -Q "ALTER LOGIN SA WITH PASSWORD=\"$(read -sp "Enter new SA password: "; echo "${REPLY}")\""


## Copia de un archivo de copia de seguridad en el contenedor

1. En primer lugar, use docker exec para crear una carpeta de copia de seguridad. El siguiente comando crea un directorio /var/opt/mssql/backup dentro del contenedor de SQL Server.

        sudo docker exec -it sql1 mkdir /var/opt/mssql/backup

2. Luego, descargue el archivo <a href=https://github.com/Microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0>WideWorldImporters-Full.bak</a> en el equipo host. Los siguientes comandos llevan al directorio home/user y descargan el archivo de copia de seguridad como wwi.bak.

        cd ~
        curl -L -o wwi.bak 'https://github.com/Microsoft/sql-server-samples/releases/download/wide-world-importers-v1.0/WideWorldImporters-Full.bak'

3. Use docker cp para copiar el archivo de copia de seguridad en el contenedor, en el directorio /var/opt/mssql/backup.

        sudo docker cp wwi.bak sql1:/var/opt/mssql/backup

## Restauración de la base de datos
El archivo de copia de seguridad ahora se encuentra dentro del contenedor. Antes de restaurar la copia de seguridad, es importante conocer los nombres de archivo lógicos y los tipos de archivo que hay dentro de la copia de seguridad. Los siguientes comandos de Transact-SQL examinan la copia de seguridad y realizan la restauración con sqlcmd en el contenedor.

1. Ejecute sqlcmd dentro del contenedor para enumerar los nombres de archivo lógicos y las rutas de acceso que hay dentro de la copia de seguridad. Esto se hace con la instrucción de Transact-SQL RESTORE FILELISTONLY.

        sudo docker exec -it sql1 /opt/mssql-tools/bin/sqlcmd -S localhost \
        -U SA -P '<YourNewStrong!Passw0rd>' \
        -Q 'RESTORE FILELISTONLY FROM DISK = "/var/opt/mssql/backup/wwi.bak"' \
        | tr -s ' ' | cut -d ' ' -f 1-2
    
    Debería ver una salida similar a la siguiente:

        LogicalName   PhysicalName
        ------------------------------------------
        WWI_Primary   D:\Data\WideWorldImporters.mdf
        WWI_UserData   D:\Data\WideWorldImporters_UserData.ndf
        WWI_Log   E:\Log\WideWorldImporters.ldf
        WWI_InMemory_Data_1   D:\Data\WideWorldImporters_InMemory_Data_1

2. Llame al comando RESTORE DATABASE para restaurar la base de datos dentro del contenedor. Especifique nuevas rutas de acceso para cada uno de los archivos del paso anterior.

        sudo docker exec -it sql1 /opt/mssql-tools/bin/sqlcmd \
        -S localhost -U SA -P '<YourNewStrong!Passw0rd>' \
        -Q 'RESTORE DATABASE WideWorldImporters FROM DISK = "/var/opt/mssql/backup/wwi.bak" WITH MOVE "WWI_Primary" TO "/var/opt/mssql/data/WideWorldImporters.mdf", MOVE "WWI_UserData" TO "/var/opt/mssql/data/WideWorldImporters_userdata.ndf", MOVE "WWI_Log" TO "/var/opt/mssql/data/WideWorldImporters.ldf", MOVE "WWI_InMemory_Data_1" TO "/var/opt/mssql/data/WideWorldImporters_InMemory_Data_1"'

Debería ver una salida similar a la siguiente:

        Processed 1464 pages for database 'WideWorldImporters', file 'WWI_Primary' on file 1.
        Processed 53096 pages for database 'WideWorldImporters', file 'WWI_UserData' on file 1.
        Processed 33 pages for database 'WideWorldImporters', file 'WWI_Log' on file 1.
        Processed 3862 pages for database 'WideWorldImporters', file 'WWI_InMemory_Data_1' on file 1.
        Converting database 'WideWorldImporters' from version 852 to the current version 869.
        Database 'WideWorldImporters' running the upgrade step from version 852 to version 853.
        Database 'WideWorldImporters' running the upgrade step from version 853 to version 854.
        Database 'WideWorldImporters' running the upgrade step from version 854 to version 855.
        Database 'WideWorldImporters' running the upgrade step from version 855 to version 856.
        Database 'WideWorldImporters' running the upgrade step from version 856 to version 857.
        Database 'WideWorldImporters' running the upgrade step from version 857 to version 858.
        Database 'WideWorldImporters' running the upgrade step from version 858 to version 859.
        Database 'WideWorldImporters' running the upgrade step from version 859 to version 860.
        Database 'WideWorldImporters' running the upgrade step from version 860 to version 861.
        Database 'WideWorldImporters' running the upgrade step from version 861 to version 862.
        Database 'WideWorldImporters' running the upgrade step from version 862 to version 863.
        Database 'WideWorldImporters' running the upgrade step from version 863 to version 864.
        Database 'WideWorldImporters' running the upgrade step from version 864 to version 865.
        Database 'WideWorldImporters' running the upgrade step from version 865 to version 866.
        Database 'WideWorldImporters' running the upgrade step from version 866 to version 867.
        Database 'WideWorldImporters' running the upgrade step from version 867 to version 868.
        Database 'WideWorldImporters' running the upgrade step from version 868 to version 869.
        RESTORE DATABASE successfully processed 58455 pages in 18.069 seconds (25.273 MB/sec).


## Comprobar la base de datos restaurada
Ejecute la consulta siguiente para mostrar una lista de nombres de bases de datos del contenedor:

    sudo docker exec -it sql1 /opt/mssql-tools/bin/sqlcmd \
    -S localhost -U SA -P '<YourNewStrong!Passw0rd>' \
    -Q 'SELECT Name FROM sys.Databases'

Debería ver **WideWorldImporters** en la lista de bases de datos.


# Crear contenedor app_plotly

	docker build -t app_plotly .

# Correr contenedor app_plotly dentro de la red "red_prueba"

	docker run --network red_prueba --network-alias app_plotly --name app_plotly --hostname app_plotly -d app_plotly


docker run --network porfolio_mysql_default --network-alias porfolio_mysql_nginx_1 --name porfolio_mysql_nginx_1 -d -p 8080:80 