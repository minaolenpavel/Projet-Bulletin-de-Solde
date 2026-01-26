using Bulletin_solde.Data.Models;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;

namespace Bulletin_solde.Data.Service
{
    public class ActivityServices
    {
        private readonly ApplicationDbContext _context;
        public ActivityServices(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<List<MonthActivity>> GetAllActivityMonths()
        {
            return await _context.MonthActivities.ToListAsync();
        }

        public List<MonthActivity> monthActivities(string jsonString)
        {
            List<MonthActivity> monthActivities = new List<MonthActivity>();
            monthActivities = JsonConvert.DeserializeObject<List<MonthActivity>>(jsonString);
            return monthActivities;
        }
    }
}
