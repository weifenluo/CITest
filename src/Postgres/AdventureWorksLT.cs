using System;
using Npgsql;

namespace CITest.Postgres;

public static class AdventureWorksLT
{
    public static int GetAddressCount()
    {
        using (var connection = new NpgsqlConnection(ConnectionString.AdventureWorksLT))
        {
            connection.Open();
            using (var command = new NpgsqlCommand("""SELECT COUNT(*) FROM "SalesLT"."Address";""", connection))
            {
                return Convert.ToInt32(command.ExecuteScalar());
            }
        }
    }
}
