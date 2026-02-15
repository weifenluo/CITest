using Xunit;

namespace CITest.Postgres;

public class AdventureWorksLTTests
{
    [Fact]
    public void GetAddressCount()
    {
        Assert.Equal(450, AdventureWorksLT.GetAddressCount());
    }
}
