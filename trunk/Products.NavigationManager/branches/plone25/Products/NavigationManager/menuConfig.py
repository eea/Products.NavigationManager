site_positions = ['default', 'eper']
menu = { 'default' : { 'title' : 'EEA website',
                       'description' : 'EEA Home website',
                       'url' : 'http://www.eea.europa.eu',
                       'positions':['eeahome','products','themes','countries','eionet','pressroom','abouteea','contacts'],
                       'children' :{ 'eeahome' : { 'title' : 'Home',
                                                   'description' : '',
                                                   'url' : 'http://www.eea.europa.eu',
                                                   'children' : None },
                                     'products' : 
                                                 { 'title' : 'Products',
                                                  'description' : '',
                                                  'url' : 'http://www.eea.europa.eu/products',
                                                  'positions': ['reportsoverview','reports','indicators','atlas','data','education','more'],
                                                  'children' :{'reportsoverview' : { 'title' : 'Overview',
                                                                             'description' : '',
                                                                             'url' : 'http://www.eea.europa.eu/products',
                                                                             'children' : None },                                         

                                                                'reports' : { 'title' : 'Reports',
                                                                             'description' : '',
                                                                             'url' : 'http://reports.eea.europa.eu/',
                                                                             'positions': ['searchreports','reportsalpha','reportsbythemes','reportsbypublishdate','reportsbylanguage','reportsbyserial','reportsbycountry'],
                                                                             'children' : {                                          
           
                                                                                'searchreports' : { 'title' : 'Latest reports / Search',
                                                                                'description' : '',
                                                                                'url' : 'http://reports.eea.europa.eu/index_html?overview=1',
                                                                               
                                                                                'children' :None},
                                                                               
                                       
                                                                                'reportsalpha' : { 'title' : 'Alphabetically',
                                                                                'description' : '',
                                                                                'url' : 'http://reports.eea.europa.eu/index_table?sort=Report',
                                                                              
                                                                                'children' :None},
                                                                               
                                       
                                                                                'reportsbythemes' : { 'title' : 'Thematically',
                                                                                'description' : '',
                                                                                'url' : 'http://reports.eea.europa.eu/index_table?sort=Thematically',
                                                                              
                                                                                'children' :None},
                                                                               
                                       
                                                                                'reportsbypublishdate' : { 'title' : 'by publish date',
                                                                                'description' : '',
                                                                                'url' : 'http://reports.eea.europa.eu/index_table?sort=Published',
                                                                            
                                                                                'children' :None},
                                                                               
                                       
                                                                                'reportsbylanguage' : { 'title' : 'by language',
                                                                                'description' : '',
                                                                                'url' : 'http://reports.eea.europa.eu/index_table?sort=Language',
                                                                              
                                                                                'children' :None},
                                                                               
                                       
                                                                                'reportsbyserial' : { 'title' : 'by serial title',
                                                                                'description' : '',
                                                                                'url' : 'http://reports.eea.europa.eu/index_table?sort=Serial',
                                                                             
                                                                                'children' :None},
                                                                               
                                       
                                                                                'reportsbycountry' : { 'title' : 'national SOE reports',
                                                                                'description' : '',
                                                                                'url' : 'http://countries.eea.europa.eu/SERIS',
                                                                                'children' :None},
                                                                              } # end of reports children
                                                                 }, #end of reports
                                                                                                                     
                                                                 'indicators' : { 'title' : 'Indicators',
                                                                                 'description' : '',
                                                                                 'url' : 'http://themes.eea.europa.eu/indicators/',
                                                                                 'positions':['indicatorswhatsnew','indicatorsalpha','indicatorsthematically','indicatorspublishdate','indicatorsassess','indicatorsdpsir','indicatorscsi','indicatorsfactsheets'],
                                                                                 'children' : {
                                                                                'indicatorswhatsnew' : { 'title' : 'What s new',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/indicators/whatsnew',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'indicatorsalpha' : { 'title' : 'Alphabetically',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/indicators/all_indicators_box?sort_by=title',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'indicatorsthematically' : { 'title' : 'Thematically',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/indicators/all_indicators_box?sort_by=theme',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'indicatorspublishdate' : { 'title' : 'by publish date',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/indicators/all_indicators_box?sort_by=publishdate',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'indicatorsassess' : { 'title' : 'by assessment',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/indicators/all_indicators_box?sort_by=assess',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'indicatorsdpsir' : { 'title' : 'by DPSIR',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/indicators/all_indicators_box?sort_by=dpsir',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'indicatorscsi' : { 'title' : 'Core Set of Indicators',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/indicators/coreset',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'indicatorsfactsheets' : { 'title' : 'Factsheets',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/indicators/all_factsheets_box',
                                                                                'children' :None},
                                                                               
                                                                              } # End of indicators children 
                                              }, # End of indicators
                                                                 'atlas' : { 'title' : 'Maps and graphs',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/atlas/default.asp?refid=2D511360-4CD0-4F20-A817-B3A882ACE323',
                                                                            'positions': ['atlasoverview','atlasalpha','atlasthematically','atlaskeywords','interactivemaps','atlasproviders','atlastermsofuse','atlasabout'],
                                                                            'children' : {                                          
           
                                                                                'atlasoverview' : { 'title' : 'What is new / Search',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/default.asp?refid=2D511360-4CD0-4F20-A817-B3A882ACE323',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlasalpha' : { 'title' : 'Alphabetically',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/available.asp?type=AZlist&amp;refid=6BDC4A55-5349-45CC-AF34-0FCFCD8504AD',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlasthematically' : { 'title' : 'Thematically',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/available.asp?type=Themes&amp;refid=094A95DE-C564-4667-B4EC-E0CDA91F8659',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlaskeywords' : { 'title' : 'by keyword',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/available.asp?type=Keywords&amp;refid=9776C9A5-1569-4F68-A113-AE921E7116E5',
                                                                                'children' :None},
                                                                               
                                                                                'interactivemaps' : { 'title' : 'Interactive maps',
                                                                                'description' : '',
                                                                                'url' : 'http://www.eea.europa.eu/quicklinks/explore-interactive-maps',
                                                                                'children' :None},
                                       
                                                                                'atlasproviders' : { 'title' : 'Providers',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/othersources.asp?refid=BCB91D9F-E308-4EC2-B31E-6D07F08C8D31',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlastermsofuse' : { 'title' : 'Terms of use',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/termsofuse.asp?refid=28A7BCF1-74D1-4617-BA54-407B2E8CFF6C',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlasabout' : { 'title' : 'About this service',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/introduction.asp?refid=D4267346-AE27-4239-A41F-1F536384AEFC',
                                                                                'children' :None},
                                                                               
                                                                               } #End of atlas children 
                                                                }, #end of atlas                                         
                                                                 'data' : { 'title' : 'Data',
                                                                           'description' : '',
                                                                           'url' : 'http://dataservice.eea.europa.eu/dataservice/default.asp?refid=911B582A-806E-4758-892E-9AB9AFB47B84',
                                                                           'positions': ['dataoverview','dataalpha','datathematically','datakeywords','dataproviders','datatermsofuse','dataabout'],
                                                                           'children' : {                                          

                                                                            'dataoverview' : { 'title' : 'What is new / Search',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/default.asp?refid=911B582A-806E-4758-892E-9AB9AFB47B84',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'dataalpha' : { 'title' : 'Alphabetically',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/available.asp?type=azlist&amp;refid=4CFE53FB-42ED-4089-BCAE-98E470A8BAD4',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'datathematically' : { 'title' : 'Thematically',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/available.asp?type=Themes&amp;refid=F163CB2B-35EE-486E-AC4A-2F8A8B97BF3C',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'datakeywords' : { 'title' : 'by keyword',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/available.asp?type=Keywords&amp;refid=735E2122-2FE5-4273-B13A-0AEFB4924985',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'dataproviders' : { 'title' : 'Providers',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/othersources.asp?refid=1DAB09F3-3694-469D-AE2E-7C9D04F2E20F',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'datatermsofuse' : { 'title' : 'Terms of use',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/termsofuse.asp?refid=932E6522-D75E-4981-A0E8-5982D5792835',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'dataabout' : { 'title' : 'About this service',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/introduction.asp?refid=56B2A53C-39D3-4BB6-AD8D-6D9BEA73C220',
                                                                            'children' :None},
                                                                           
                                                                              } #End of children 
                                                                 },  # end of dataservice                                       
                                                                'education' : { 'title' : 'Education',
                                                                              'description' : '',
                                                                              'url' : 'http://www.eea.europa.eu/promotions/educational',
                                                                              'children' : None },                                           
                                                              'more' : { 'title' : 'More products ...',
                                                                        'description' : '',
                                                                        'url' : 'http://www.eea.europa.eu/products',
                                                                        'positions':['epaedia','seris','producteper','eunis','econinstr','calendar'],
                                                                        'children' :{                                          
                                                                        'epaedia' : { 'title' : 'Epaedia - environment explained',
                                                                        'description' : '',
                                                                        'url' : 'http://epaedia.eea.europa.eu',
                                                                        'children' :None},
                                                                       
                               
                                                                        'seris' : { 'title' : 'SERIS - Links to national SOE reports',
                                                                        'description' : '',
                                                                        'url' : 'http://countries.eea.europa.eu/SERIS',
                                                                        'children' :None},
                                                                       
                               
                                                                        'producteper' : { 'title' : 'EPER - Pollutant register (EC / EEA)',
                                                                        'description' : '',
                                                                        'url' : 'http://eper.cec.eu.int',
                                                                        'children' :None},
                                                                       
                               
                                                                        'eunis' : { 'title' : 'EUNIS - Find species, habitats and sites',
                                                                        'description' : '',
                                                                        'url' : 'http://eunis.eea.europa.eu/',
                                                                        'children' :None},
                                                                       
                               
                                                                        'econinstr' : { 'title' : 'Economic instruments (OECD / EEA)',
                                                                        'description' : '',
                                                                        'url' : 'http://www2.oecd.org/ecoinst/queries/',
                                                                        'children' :None},
                                                                       
                               
                                                                        'calendar' : { 'title' : 'Environmental events calendar',
                                                                        'description' : '',
                                                                        'url' : 'http://www.eea.europa.eu/Events/Calendar',
                                                                        'children' :None},
                                                      
                                                                      } #End of children
                                                }, #End of More   
                                         } # End products children
                                      }, # End Products
                                      'themes' : { 'title' : 'Themes',
                                                  'description' : '',
                                                  'url' : 'http://themes.eea.europa.eu',
                                                  'positions' :['agriculture','air','biodiversity','chemicals','climate','coastsseas','energy','fisheries','households','humanhealth','industry','noise','ozone','soil','transport','urban','waste','water','morethemes'],
                                                  'children' :{
                                                               'agriculture' : { 'title' : 'Agriculture',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/Sectors_and_activities/agriculture',
                                                                                'children' : None },                                         
                                                               'air' : { 'title' : 'Air',
                                                                                         'description' : '',
                                                                                         'url' : 'http://themes.eea.europa.eu/Specific_media/air',
                                                                                         'children' : None },                                         
                                                               'biodiversity' : { 'title' : 'Biodiversity change',
                                                                                 'description' : '',
                                                                                 'url' : 'http://themes.eea.europa.eu/Environmental_issues/biodiversity',
                                                                                 'children' : None },                                         

                                                                'chemicals' : { 'title' : 'Chemicals',
                                                                               'description' : '',
                                                                               'url' : 'http://themes.eea.europa.eu/Environmental_issues/chemicals',
                                                                               'children' : None },                                         

                                                                'climate' : { 'title' : 'Climate change',
                                                                             'description' : '',
                                                                             'url' : 'http://themes.eea.europa.eu/Environmental_issues/climate',
                                                                             'children' : None },                                         

                                                                'coastsseas' : { 'title' : 'Coasts and seas ',
                                                                                'description' : '',
                                                                                'url' : 'http://themes.eea.europa.eu/Specific_areas/coast_sea',
                                                                                'children' : None },                                         

                                                                'energy' : { 'title' : 'Energy',
                                                                            'description' : '',
                                                                            'url' : 'http://themes.eea.europa.eu/Sectors_and_activities/energy',
                                                                            'children' : None },                                         
                                                                'fisheries' : { 'title' : 'Fisheries',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Sectors_and_activities/fishery',
                                                                'children' : None },                                         
                
                                                                'households' : { 'title' : 'Households',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Sectors_and_activities/households',
                                                                'children' : None },                                         
                
                                                                'humanhealth' : { 'title' : 'Human health',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Environmental_issues/human',
                                                                'children' : None },                                         
                
                                                                'industry' : { 'title' : 'Industry',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Sectors_and_activities/industry',
                                                                'children' : None },                                         
                
                                                                'noise' : { 'title' : 'Noise',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Environmental_issues/noise',
                                                                'children' : None },                                         
                
                                                                'ozone' : { 'title' : 'Ozone depletion',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Environmental_issues/ozone',
                                                                'children' : None },                                         
                
                                                                'soil' : { 'title' : 'Soil',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Specific_media/soil',
                                                                'children' : None },                                         
                
                                                                'transport' : { 'title' : 'Transport',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Sectors_and_activities/transport',
                                                                'children' : None },                                         
                
                                                                'urban' : { 'title' : 'Urban environment',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Specific_areas/urban',
                                                                'children' : None },                                         
                
                                                                'waste' : { 'title' : 'Waste',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Environmental_issues/waste',
                                                                'children' : None },                                         
                
                                                                'water' : { 'title' : 'Water',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu/Specific_media/water',
                                                                'children' : None },                                         
                
                                                                'morethemes' : { 'title' : 'More themes ...',
                                                                'description' : '',
                                                                'url' : 'http://themes.eea.europa.eu',
                                                                'children' : None },
                                                               } # End of themes children
                                     }, # End of themes 
                                     
                                   'countries' : 
                                           { 'title' : 'Countries',
                                            'description' : '',
                                            'url' : 'http://countries.eea.europa.eu/SERIS',
                                            'children' :None
                                    }, # End of countries
 							   'eionet' : 
                                       { 'title' : 'Eionet',
                                       'description' : '',
                                       'url' : 'http://eionet.europa.eu/',
                                       'children' :None
                                      },   # End of Eionet 
                                     'pressroom' : 
                                   { 'title' : 'Press room',
                                   'description' : '',
                                   'url' : 'http://www.eea.europa.eu/pressroom',
                                   'positions':['pressoverview','pressreleases','announcements','latestreports','pressimages','speeches','presscontact'],
                                   'children' :{
                                                'pressoverview' : { 'title' : 'Overview',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/pressroom',
                                                'children' : None },                                         

                                                'pressreleases' : { 'title' : 'Press releases',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/pressroom/newsreleases',
                                                'children' : None },                                         
                                       
                                                'latestreports' : { 'title' : 'Latest reports',
                                                'description' : '',
                                                'url' : 'http://reports.eea.eu.int/',
                                                'children' : None },                                         

                                                'pressimages' : { 'title' : 'Images for press',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/pressroom/pictures',
                                                'children' : None },                                         

                                                'speeches' : { 'title' : 'Speeches',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/pressroom/speeches',
                                                'children' : None },                                         

                                                'presscontact' : { 'title' : 'Press contact',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/pressroom#presscontact',
                                                'children' : None },                                         

                                               } 
                                     }, # End of press room

                            'abouteea' : 
                                   { 'title' : 'About EEA',
                                   'description' : '',
                                   'url' : 'http://www.eea.europa.eu/aboutus',
                                   'positions':['abouteeaoverview','organisation','abouteeadocuments','keypartners','abouteeanetworks','jobs','calls4tender'],
                                   'children' :{
                                                'abouteeaoverview' : { 'title' : 'Overview',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/aboutus',
                                                'children' : None },                                         

                                                'organisation' : { 'title' : 'Organisation',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/organisation/',
                                                'children' : None },                                                                         

                                                'abouteeadocuments' : { 'title' : 'Documents',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/documents/',
                                                'children' : None },                                         

                                                'keypartners' : { 'title' : 'Key partners',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/links/keypart.html',
                                                'children' : None },                                         

                                                'abouteeanetworks' : { 'title' : 'Networks',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/networks',
                                                'children' : None },                                         

                                                'jobs' : { 'title' : 'Job opportunities',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/organisation/jbs/index.html',
                                                'children' : None },                                         

                                                'calls4tender' : { 'title' : 'Contract opportunities',
                                                'description' : '',
                                                'url' : 'http://www.eea.europa.eu/tenders',
                                                'children' : None },                                         

                                               } 
                                     }, # End of about EEA

                                     'contacts' : 
                                       { 'title' : 'Contact us',
                                       'description' : '',
                                       'url' : 'http://www.eea.europa.eu/address.html',
                                       'children' :{
                                               } 
                                      },   # End of contact us          
                                 } # End of default children
                       }, # End default
         'eper' : { 'title' : 'Eper website',
                       'description' : 'Eper home website',
                       'url' : 'http://eper.ec.europa.eu',
                       'positions':['eperhome','searcheper'],
                       'children' :{ 'eperhome' : { 'title' : 'Home',
                                                   'description' : '',
                                                   'url' : '',
                                                   'children' : None },
                                     'searcheper' : { 'title' : 'Search EPER',
                                                   'description' : 'Search EPER database',
                                                   'url' : '',
                                                   'children' : None }
                                       }
                       }, # End of Eper menu
         'dataservice_intranet' : { 'title' : 'Data service - Intranet',
                       'description' : 'Data service - Intranet',
                       'url' : 'http://gnat/dataservice/',
                       'positions':['data'],
                       'children' :{'data' : { 'title' : 'Data',
                                                                           'description' : '',
                                                                           'url' : 'http://dataservice.eea.europa.eu/dataservice/default.asp?refid=911B582A-806E-4758-892E-9AB9AFB47B84',
                                                                           'positions': ['dataoverview','dataalpha','datathematically','datakeywords','dataproviders','datatermsofuse','dataabout'],
                                                                           'children' : {                                          

                                                                            'dataoverview' : { 'title' : 'What is new / Search',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/default.asp?refid=911B582A-806E-4758-892E-9AB9AFB47B84',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'dataalpha' : { 'title' : 'Alphabetically',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/available.asp?type=azlist&amp;refid=4CFE53FB-42ED-4089-BCAE-98E470A8BAD4',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'datathematically' : { 'title' : 'Thematically',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/available.asp?type=Themes&amp;refid=F163CB2B-35EE-486E-AC4A-2F8A8B97BF3C',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'datakeywords' : { 'title' : 'by keyword',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/available.asp?type=Keywords&amp;refid=735E2122-2FE5-4273-B13A-0AEFB4924985',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'dataproviders' : { 'title' : 'Providers',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/othersources.asp?refid=1DAB09F3-3694-469D-AE2E-7C9D04F2E20F',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'datatermsofuse' : { 'title' : 'Terms of use',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/termsofuse.asp?refid=932E6522-D75E-4981-A0E8-5982D5792835',
                                                                            'children' :None},
                                                                           
                                   
                                                                            'dataabout' : { 'title' : 'About this service',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/dataservice/introduction.asp?refid=56B2A53C-39D3-4BB6-AD8D-6D9BEA73C220',
                                                                            'children' :None},
                                                                            } #End of data children 
                                        }, #End of data 
                                        'atlas' : { 'title' : 'Maps and graphs',
                                                                            'description' : '',
                                                                            'url' : 'http://dataservice.eea.europa.eu/atlas/default.asp?refid=2D511360-4CD0-4F20-A817-B3A882ACE323',
                                                                            'positions': ['atlasoverview','atlasalpha','atlasthematically','atlaskeywords','atlasproviders','atlastermsofuse','atlasabout'],
                                                                            'children' : {                                          
           
                                                                                'atlasoverview' : { 'title' : 'What is new / Search',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/default.asp?refid=2D511360-4CD0-4F20-A817-B3A882ACE323',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlasalpha' : { 'title' : 'Alphabetically',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/available.asp?type=AZlist&amp;refid=6BDC4A55-5349-45CC-AF34-0FCFCD8504AD',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlasthematically' : { 'title' : 'Thematically',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/available.asp?type=Themes&amp;refid=094A95DE-C564-4667-B4EC-E0CDA91F8659',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlaskeywords' : { 'title' : 'by keyword',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/available.asp?type=Keywords&amp;refid=9776C9A5-1569-4F68-A113-AE921E7116E5',
                                                                                'children' :None},
                                                                             
                                                                                'atlasproviders' : { 'title' : 'Providers',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/othersources.asp?refid=BCB91D9F-E308-4EC2-B31E-6D07F08C8D31',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlastermsofuse' : { 'title' : 'Terms of use',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/termsofuse.asp?refid=28A7BCF1-74D1-4617-BA54-407B2E8CFF6C',
                                                                                'children' :None},
                                                                               
                                       
                                                                                'atlasabout' : { 'title' : 'About this service',
                                                                                'description' : '',
                                                                                'url' : 'http://dataservice.eea.europa.eu/atlas/introduction.asp?refid=D4267346-AE27-4239-A41F-1F536384AEFC',
                                                                                'children' :None},
                                                                               } #End of atlas children 
                                                                }, #end of atlas                             
                             } #End of dataservice intranet children 
                       } # End of intranet dataservice
            } #End of menu
