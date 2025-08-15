import React from 'react';
import { Card, CardContent } from './ui/card';
import { Search, Target, TrendingUp, PieChart } from 'lucide-react';

const iconMap = {
  Search,
  Target, 
  TrendingUp,
  PieChart
};

const Services = ({ data }) => {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-5xl font-bold text-gray-900 mb-6">
            Как я работаю с вашей стоматологией
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Проверенная методология, которая приносит стабильные результаты 
            стоматологическим клиникам уже более 6 лет
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {data.map((service, index) => {
            const Icon = iconMap[service.icon];
            return (
              <Card key={service.id} className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg hover:-translate-y-2">
                <CardContent className="p-8 text-center">
                  <div className="mb-6">
                    <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-600 transition-colors duration-300">
                      <Icon className="h-8 w-8 text-blue-600 group-hover:text-white transition-colors duration-300" />
                    </div>
                    <div className="text-2xl font-bold text-blue-600 mb-2">
                      0{index + 1}
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-4">
                    {service.title}
                  </h3>
                  
                  <p className="text-gray-600 leading-relaxed">
                    {service.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Process timeline */}
        <div className="mt-20">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Весь процесс займет всего 3-5 дней
            </h3>
            <p className="text-gray-600">
              От первого звонка до запуска рекламы
            </p>
          </div>
          
          <div className="relative">
            <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-blue-200"></div>
            
            <div className="space-y-12">
              {[
                { day: "День 1", title: "Консультация и анализ", desc: "Изучаем вашу клинику, конкурентов и текущую ситуацию" },
                { day: "День 2-3", title: "Стратегия и настройка", desc: "Создаем стратегию продвижения и настраиваем кампании" },
                { day: "День 4-5", title: "Запуск и первые результаты", desc: "Запускаем рекламу и получаем первые заявки" }
              ].map((step, index) => (
                <div key={index} className={`flex items-center ${index % 2 === 0 ? 'justify-start' : 'justify-end'}`}>
                  <div className={`w-5/12 ${index % 2 === 0 ? 'pr-8 text-right' : 'pl-8 text-left'}`}>
                    <Card className="p-6 shadow-lg border-0">
                      <div className="space-y-2">
                        <div className="text-blue-600 font-bold">{step.day}</div>
                        <h4 className="font-bold text-gray-900">{step.title}</h4>
                        <p className="text-gray-600 text-sm">{step.desc}</p>
                      </div>
                    </Card>
                  </div>
                  
                  <div className="w-8 h-8 bg-blue-600 rounded-full border-4 border-white shadow-lg z-10 flex items-center justify-center">
                    <div className="w-2 h-2 bg-white rounded-full"></div>
                  </div>
                  
                  <div className="w-5/12"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Services;