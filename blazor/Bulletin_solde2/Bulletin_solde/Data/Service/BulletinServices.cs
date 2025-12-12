using Bulletin_solde.Data.Models;
using Bulletin_solde.Data.Service;
using Bulletin_solde.Data.Services;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;

namespace Bulletin_solde.Data.Services
{
    public class BulletinServices
    {
        private readonly ApplicationDbContext _context;
        private readonly StatisticsServices _statsServices;
        public BulletinServices(ApplicationDbContext context, StatisticsServices statisticsServices)
        {
            _context = context;
            _statsServices = statisticsServices;
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

        public async Task<Tuple<int, int>> GetMissingMonthCount()
        {
            DateTime dateIncorpo = new DateTime(2023, 11, 1);
            Tuple<DateTime, int> lastPayment = await TimeSinceLastPayment();
            DateTime lastPaymentDate = lastPayment.Item1;

            int totalMonths = (int)((lastPaymentDate - dateIncorpo).TotalDays / 30);
            int bulletinsCount = await _statsServices.GetCountAsync<Bulletin>(b => b.Id);
            int missingMonths = totalMonths - bulletinsCount;
            return Tuple.Create(missingMonths, totalMonths);
        }

        public async Task<Tuple<DateTime, int>> TimeSinceLastPayment()
        {
            List<DateTime> bulletinDates = await _context.Bulletins.Select(b => b.Date).ToListAsync();
            bulletinDates.Order();
            DateTime lastPayment = bulletinDates.Last();
            double totalDays = (DateTime.Now - lastPayment).TotalDays;
            int timeSinceLastPayment = (int)totalDays;
            return Tuple.Create(lastPayment, timeSinceLastPayment);
        }
    }
}