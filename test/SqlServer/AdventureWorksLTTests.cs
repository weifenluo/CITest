using Xunit;

namespace CITest.SqlServer;

public class AdventureWorksLTTests
{
    [Fact]
    public void GetAddressCount()
    {
        Assert.Equal(450, AdventureWorksLT.GetAddressCount());
    }
}
