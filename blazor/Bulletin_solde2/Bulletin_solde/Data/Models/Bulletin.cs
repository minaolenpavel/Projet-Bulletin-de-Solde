using System.ComponentModel.DataAnnotations.Schema;
using System.Data;
using System.Runtime.CompilerServices;

namespace Bulletin_solde.Data.Models
{
    public class Bulletin
    {
        public int Id { get; set; }
        public int Year { get; set; }
        public int Month { get; set; }
        public double Amount { get; set; }
        public string FilePath { get; set; }
        public int ArrivalDay { get; set; }

        [NotMapped] // EF Core ignores this field
        public DateTime Date => new DateTime(Year, Month, ArrivalDay);

    }
}