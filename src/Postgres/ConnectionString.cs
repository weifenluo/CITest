using System;

namespace CITest.Postgres;

internal static class ConnectionString
{
    private static readonly string s_localServer
        = Environment.ExpandEnvironmentVariables("Server=%OpenEntity_Postgres_Server%;UserId=%OpenEntity_Postgres_User%;Password=%OpenEntity_Postgres_Password%;TrustServerCertificate=true");

    public static string Of(string dbName) => s_localServer + $";Database={dbName}";

    public static string AdventureWorksLT { get; } = Of("AdventureWorksLT");
}
