using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography.X509Certificates;
using System;
using System.Runtime.CompilerServices;
using Bulletin_solde.Data.Models;
using MudBlazor;

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
            // Sum the values
            double sqrtDistSum = powDist.Sum();
            // Divide by the number of data points
            double result = Math.Sqrt(sqrtDistSum / await GetCountBulletins());
            return Math.Round(result, 3);
        }
        public async Task<double> GetMedianIncome()
        {
            List<double> amounts = await _context.Bulletins.Select(b => b.Amount).ToListAsync();
            amounts.Sort();
            int mid = amounts.Count / 2;
            double median = 0;
            if(mid%2 != 0)
            {
                median = amounts[mid];
            }
            else
            {
                median = (amounts[mid - 1] + amounts[mid] / 2);
            }
            return median;
        }

        public async Task<Tuple<int, int>> GetMissingMonthCount()
        {
            DateTime dateIncorpo = new DateTime(2023, 11, 1);
            Tuple<DateTime, int> lastPayment = await TimeSinceLastPayment();
            DateTime lastPaymentDate = lastPayment.Item1;
            
            int totalMonths = (int)((lastPaymentDate - dateIncorpo).TotalDays/30);
            int bulletinsCount = await GetCountBulletins();
            int missingMonths = totalMonths - bulletinsCount;
            return Tuple.Create(missingMonths, totalMonths);
        }

        public async Task<Tuple<DateTime, int>> TimeSinceLastPayment()
        {
            List < DateTime> bulletinDates = await _context.Bulletins.Select(b => b.Date).ToListAsync();
            bulletinDates.Order();
            DateTime lastPayment = bulletinDates.Last();
            double totalDays = (DateTime.Now - lastPayment).TotalDays;
            int timeSinceLastPayment = (int)totalDays;
            return Tuple.Create(lastPayment,timeSinceLastPayment);
        }

        public async Task<string> CommentSTD()
        {
            double std = await GetStandardDeviationIncome();
            double max = await GetMaxEndIncome();
            double min = await GetMinStartIncome();
            double range = max - min;
            if (range == 0)
            {
                return "Pas de variabilité, les valeurs max et min sont égales";
            }
            double ratio = std / range;
            if (ratio < 0.1)
            {
                return "variabilité très faible";
            }
            else if (ratio < 0.2)
            {
                return "variabilité faible";
            }
            else if(ratio < 0.3)
            {
                return "variabilité modérée";
            }
            else if(ratio < 0.5)
            {
                return "haute variabilité";
            }
            else
            {
                return "très haute variabilité";
            }
        }
    }
}
