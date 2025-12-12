using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography.X509Certificates;
using System;
using System.Runtime.CompilerServices;
using Bulletin_solde.Data.Models;
using MudBlazor;
using System.Linq.Expressions;

namespace Bulletin_solde.Data.Service
{
    public class StatisticsServices
    {
        private readonly ApplicationDbContext _context;

        public StatisticsServices(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<double> GetTotalAsync<TEntity>(
            Expression<Func<TEntity, double>> selector)
            where TEntity : class
        {
            double total = (double)await _context.Set<TEntity>()
                .Select(selector)
                .SumAsync();
            return Math.Round((double)total,2);
        }
        public async Task<double> GetAverageAsync<TEntity>(
            Expression<Func<TEntity, double>> selector)
            where TEntity : class
        {
            double average = (double)await _context.Set<TEntity>()
                .Select(selector)
                .AverageAsync();
            return Math.Round(average, 2);
        }
        public async Task<double> GetMinAsync<TEntity>(
            Expression<Func<TEntity, double>> selector)
            where TEntity : class
        {
            double min = (double)await _context.Set<TEntity>()
                .Select(selector)
                .MinAsync();
            return Math.Round(min, 2);
        }
        public async Task<double> GetMaxAsync<TEntity>(
            Expression<Func<TEntity, double>> selector) 
            where TEntity : class
        {
            double max = (double)await _context.Set<TEntity>()
                .Select(selector)
                .MaxAsync();
            return Math.Round(max, 2);
        }
        public async Task<int> GetCountAsync<TEntity>(
            Expression<Func<TEntity, int>> selector)
            where TEntity : class
        {
            int count = await _context.Set<TEntity>()
                .Select(selector)
                .Distinct()
                .CountAsync();
            return count;
        }
        public async Task<double> GetStandardDeviationAsync<TEntity>(
            Expression<Func<TEntity, double>> selector)
            where TEntity : class
        {
            List<TEntity> entities = await _context.Set<TEntity>()
                .ToListAsync();
            var set = _context.Set<TEntity>();
            // Find the mean
            double avg = await _context.Set<TEntity>()
                .Select(selector)
                .AverageAsync();
            // For each data point, find the square root of its distance to the mean
            var param = selector.Parameters[0];
            var squaredBody = Expression.Multiply(selector.Body, selector.Body);
            var squareSelector = Expression.Lambda<Func<TEntity, double>>(squaredBody, param);
            var averageSquare = await set.Select(squareSelector).AverageAsync();
            var std = Math.Sqrt((double)(averageSquare - avg * avg));
            // Sum the values
            // Divide by the number of data points
            
            return Math.Round(std, 3);
        }
        public async Task<double> GetMedianAsync<TEntity>(
            Expression<Func<TEntity, double>> selector)
            where TEntity : class
        {
            try
            {
                List<double> numbers = await _context.Set<TEntity>()
                    .Select(selector)
                    .ToListAsync();
                numbers.Sort();
                int mid = numbers.Count / 2;
                double median = 0;
                if (mid % 2 != 0)
                {
                    median = numbers[mid];
                }
                else
                {
                    median = (numbers[mid - 1] + numbers[mid] / 2);
                }
                return median;
            }
            catch
            {
                return 0;
            }
            
        }

        public async Task<string> CommentSTD<TEntity>(
            Expression<Func<TEntity, double>> selector)
            where TEntity : class
        {
            double std = await GetStandardDeviationAsync<TEntity>(selector);
            double max = await GetMaxAsync<TEntity>(selector);
            double min = await GetMinAsync<TEntity>(selector);
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
