using Bulletin_solde.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace Bulletin_solde.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
        {
        }
        public DbSet<Bulletin> Bulletin { get; set; }
    }
}
