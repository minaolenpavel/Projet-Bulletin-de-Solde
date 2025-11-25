namespace Bulletin_solde.Data.Models
{
    public class Bulletin
    {
        public int Id { get; set; }
        public int Year { get; set; }
        public int Month { get; set; }
        public string MonthText { get; set; }
        public string Period { get; set; }
        public decimal Amount { get; set; }
        public string FilePath { get; set; }

    }
}