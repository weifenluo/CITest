using System;
using Microsoft.Data.SqlClient;

namespace CITest.SqlServer;

public static class AdventureWorksLT
{
    public static int GetAddressCount()
    {
        using (var connection = new SqlConnection(ConnectionString.AdventureWorksLT))
        {
            connection.Open();
            using (var command = new SqlCommand("SELECT COUNT(*) FROM SalesLT.Address", connection))
            {
                return Convert.ToInt32(command.ExecuteScalar());
            }
        }
    }
}
