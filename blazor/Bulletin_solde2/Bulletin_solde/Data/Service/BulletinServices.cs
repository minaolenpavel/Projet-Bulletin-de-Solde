using Bulletin_solde.Data.Models;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;

namespace Bulletin_solde.Data.Services
{
    public class BulletinServices
    {
        private readonly ApplicationDbContext _context;
        public BulletinServices(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<List<Bulletin>> GetAllBulletins()
        {
            return await _context.Bulletins.ToListAsync();
        }

        public async Task AddBulletin(Bulletin bulletin)
        {
            _context.Bulletins.Add(bulletin);
            await _context.SaveChangesAsync();
        }

        public Bulletin? ParseJson(string jsonString)
        {
            Bulletin? bulletin = null;
            bulletin = JsonConvert.DeserializeObject<Bulletin>(jsonString);
            return bulletin;
        }

    }
}