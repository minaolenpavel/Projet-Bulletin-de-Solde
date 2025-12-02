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
        public string Period { get; set; }
        public decimal Amount { get; set; }
        public string FilePath { get; set; }

        [NotMapped] // EF Core ignores this field
        public DateTime Date => new DateTime(Year, Month, 1);

    }
}