import React, { useState } from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ArrowRight, TrendingUp, DollarSign, Users, Calendar } from 'lucide-react';

const Cases = ({ data }) => {
  const [selectedCase, setSelectedCase] = useState(data[0]);

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="bg-green-100 text-green-800 px-4 py-2 text-sm mb-4">
            Проверенные результаты
          </Badge>
          <h2 className="text-3xl lg:text-5xl font-bold text-gray-900 mb-6">
            Реальные кейсы моих клиентов
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Каждый кейс — это история успеха стоматологической клиники, 
            которая получила стабильный поток новых пациентов
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Case selector */}
          <div className="lg:col-span-1">
            <div className="space-y-4">
              {data.map((caseItem) => (
                <Card 
                  key={caseItem.id}
                  className={`cursor-pointer transition-all duration-300 border-2 ${
                    selectedCase.id === caseItem.id 
                      ? 'border-blue-500 shadow-xl bg-blue-50' 
                      : 'border-gray-200 hover:border-gray-300 hover:shadow-lg'
                  }`}
                  onClick={() => setSelectedCase(caseItem)}
                >
                  <CardContent className="p-6">
                    <h3 className="font-bold text-gray-900 mb-2">
                      {caseItem.title}
                    </h3>
                    <p className="text-gray-600 text-sm mb-4">
                      {caseItem.subtitle}
                    </p>
                    <div className="flex items-center text-green-600 font-semibold text-sm">
                      <TrendingUp className="h-4 w-4 mr-1" />
                      {caseItem.results.growth}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Selected case details */}
          <div className="lg:col-span-2">
            <Card className="shadow-2xl border-0 overflow-hidden">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-8">
                <h3 className="text-3xl font-bold mb-2">{selectedCase.title}</h3>
                <p className="text-blue-100 text-lg mb-4">{selectedCase.subtitle}</p>
                <p className="text-lg">{selectedCase.description}</p>
              </div>
              
              <CardContent className="p-8">
                {/* Results */}
                <div className="mb-8">
                  <h4 className="text-xl font-bold text-gray-900 mb-6">Результаты работы</h4>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="bg-green-50 rounded-2xl p-6 text-center">
                      <Users className="h-8 w-8 text-green-600 mx-auto mb-3" />
                      <div className="text-3xl font-bold text-green-600 mb-1">
                        {selectedCase.results.leads}
                      </div>
                      <div className="text-gray-600">заявок в месяц</div>
                    </div>
                    
                    <div className="bg-blue-50 rounded-2xl p-6 text-center">
                      <DollarSign className="h-8 w-8 text-blue-600 mx-auto mb-3" />
                      <div className="text-3xl font-bold text-blue-600 mb-1">
                        {selectedCase.results.cost_per_lead}₽
                      </div>
                      <div className="text-gray-600">стоимость заявки</div>
                    </div>
                    
                    <div className="bg-purple-50 rounded-2xl p-6 text-center">
                      <Calendar className="h-8 w-8 text-purple-600 mx-auto mb-3" />
                      <div className="text-3xl font-bold text-purple-600 mb-1">
                        {selectedCase.results.budget.toLocaleString()}₽
                      </div>
                      <div className="text-gray-600">бюджет в месяц</div>
                    </div>
                    
                    <div className="bg-orange-50 rounded-2xl p-6 text-center">
                      <TrendingUp className="h-8 w-8 text-orange-600 mx-auto mb-3" />
                      <div className="text-3xl font-bold text-orange-600 mb-1">
                        {selectedCase.results.growth}
                      </div>
                      <div className="text-gray-600">рост пациентов</div>
                    </div>
                  </div>
                </div>

                {/* Process */}
                <div className="mb-8">
                  <h4 className="text-xl font-bold text-gray-900 mb-4">Что делали</h4>
                  <p className="text-gray-600 mb-6">{selectedCase.tasks}</p>
                  
                  <div className="space-y-3">
                    {selectedCase.process.map((step, index) => (
                      <div key={index} className="flex items-center p-4 bg-gray-50 rounded-lg">
                        <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-4">
                          {index + 1}
                        </div>
                        <span className="text-gray-800">{step}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* CTA */}
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 text-center">
                  <h5 className="text-lg font-bold text-gray-900 mb-2">
                    Хотите такие же результаты?
                  </h5>
                  <p className="text-gray-600 mb-4">
                    Обсудим ваш проект и составим план продвижения
                  </p>
                  <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 font-semibold group">
                    Получить консультацию
                    <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Cases;