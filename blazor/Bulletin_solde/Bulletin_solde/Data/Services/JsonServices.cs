using Bulletin_solde.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace Bulletin_solde.Data.Services
{
    public class JsonServices
    {
        private readonly ApplicationDbContext _context;
        public JsonServices(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<List<Bulletin>> GetAllBulletins()
        {
            return await _context.Bulletin.ToListAsync();
        }

        public async Task AddBulletin(Bulletin bulletin)
        {
            _context.Bulletin.Add(bulletin);
            await _context.SaveChangesAsync();
        }

    }
}
