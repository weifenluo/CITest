using System;

namespace CITest.SqlServer;

internal static class ConnectionString
{
    public static string LocalServer { get; }
        = Environment.ExpandEnvironmentVariables("Server=%OpenEntity_MSSQL_Server%;User Id=sa;Password=%OpenEntity_MSSQL_Password%;TrustServerCertificate=true");

    public static string Of(string dbName) => LocalServer + $";Database={dbName}";

    public static string AdventureWorksLT { get; } = Of("AdventureWorksLT");
}

