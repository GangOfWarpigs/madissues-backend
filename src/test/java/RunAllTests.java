import org.junit.platform.suite.api.SelectPackages;
import org.junit.platform.suite.api.SuiteDisplayName;
import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(org.junit.platform.runner.JUnitPlatform.class)
@SuiteDisplayName("JUnit Platform Suite Demo")
@SelectPackages("org.madissues")
public class RunAllTests {
}
