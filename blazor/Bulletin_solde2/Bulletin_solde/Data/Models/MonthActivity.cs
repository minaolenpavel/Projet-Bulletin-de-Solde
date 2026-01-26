namespace Bulletin_solde.Data.Models
{
    public class MonthActivity
    {
        public int Id { get; set; }
        public int Year { get; set; }
        public int Month { get; set; }
        public List<ActivityPeriod> Periods { get; set; }
    }
}
