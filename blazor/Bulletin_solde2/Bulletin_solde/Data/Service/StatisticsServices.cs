using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography.X509Certificates;
using System;

namespace Bulletin_solde.Data.Service
{
    public class StatisticsServices
    {
        private readonly ApplicationDbContext _context;

        public StatisticsServices(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<double> GetTotalIncome()
        {
            // Amount is declared as decimal in C# class but sqlite does not support summing decimal
            // So we need to convert to double
            double total = await _context.Bulletins.Select(b => b.Amount).SumAsync();
            return Math.Round(total,2);
        }
        public async Task<double> GetAverageIncome()
        {
            double average = await _context.Bulletins.Select(b => b.Amount).AverageAsync();
            return Math.Round(average, 2);
        }
        public async Task<double> GetMinStartIncome()
        {
            double minStart = await _context.Bulletins.Select(b => b.Amount).MinAsync();
            return Math.Round(minStart, 2);
        }
        public async Task<double> GetMaxEndIncome()
        {
            double maxEnd = await _context.Bulletins.Select(b => b.Amount).MaxAsync();
            return Math.Round(maxEnd, 2);
        }
    }
}
