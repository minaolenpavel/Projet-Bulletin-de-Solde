using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography.X509Certificates;
using System;
using System.Runtime.CompilerServices;
using Bulletin_solde.Data.Models;

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
        public async Task<int> GetCountBulletins()
        {
            int countBulletins = await _context.Bulletins.Select(b =>b).Distinct().CountAsync();
            return countBulletins;
        }
        public async Task<double> GetStandardDeviationIncome()
        {
            List<Bulletin> bulletins = await _context.Bulletins.ToListAsync();
            // Find the mean
            double avg = await _context.Bulletins.Select(b => b.Amount).AverageAsync();
            // For each data point, find the square root of its distance to the mean
            var powDist = bulletins.Select(b => Math.Pow(Math.Abs(b.Amount - avg), 2)).ToList();
            double sqrtDistSum = powDist.Sum();
            double result = Math.Sqrt(sqrtDistSum / await GetCountBulletins());
            return Math.Round(result, 3);
        }
    }
}
