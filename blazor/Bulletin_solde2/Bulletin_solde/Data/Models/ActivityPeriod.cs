namespace Bulletin_solde.Data.Models
{
    public class ActivityPeriod
    {
        public int Id { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public int DaysCount { get; set; }
    }
}
