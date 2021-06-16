\ProvidesClass{sprawozdanie-agh} 
\ProcessOptions\LoadClass[a4paper,16pt]{extarticle} 

% Pakiety
\RequirePackage[polish]{babel}
\RequirePackage[T1]{fontenc}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage[usenames]{color}
\RequirePackage{fancyhdr}
\RequirePackage{url}
\RequirePackage{titlesec}
\RequirePackage{tocloft}
\usepackage{ifthen}
\geometry{verbose,tmargin=2.5cm,bmargin=2.5cm,lmargin=2cm,rmargin=2cm}
\frenchspacing % włączenie odpowiednich spacji po kropkach
\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}

% Przepisanie parametrów
\def\przedmiot#1	{\gdef\@przedmiot{#1}}
\def\tytul#1		{\gdef\@tytul{#1}}
\def\podtytul#1		{\gdef\@podtytul{#1}}
\def\kierunek#1		{\gdef\@kierunek{#1}}
\def\autor#1		{\gdef\@autor{#1}}
\def\email#1		{\gdef\@email{#1}}
\def\data#1			{\gdef\@data{#1}}

% Domyślny kierunek
\ifx \@kierunek \undefined
	\def \@kierunek {informatyka}
\fi

% Strona tytułowa
\newcommand{\stronatytulowa}{
	\begin{titlepage}
		\begin{center}
			%\vspace*{3cm}
		
			% Góra strony
			\textsc{\LARGE \bfseries akademia g{\'o}rniczo-hutnicza}\\[0.2cm]
			\textsc{\large wydzia\l \space elektrotechniki, automatyki, informatyki i elektroniki}\\
			\textsc{\large kierunek \@kierunek}\\[1.5cm]
			\begin{figure}[h!]
				\begin{center}
					\leavevmode
					\includegraphics[scale=0.8, trim = 0mm 0mm 0mm 0mm, clip]{logo-agh.jpg}
				\end{center}
			\end{figure}
			\vspace{2cm}
			\textsc{\Large \@przedmiot}

			% Tytuł
			\HRule \\[0.4cm]{
				\Large \bfseries \@tytul\\[0.3cm]
				\normalsize \@podtytul
			}\\[0.4cm]
			\HRule \\[1.5cm]
			
			% Autor
			\begin{minipage}{0.7\textwidth}
				\begin{center}
					\large
					%\emph{Autor:}\\
					\@autor
					\ifx \@email \undefined
					\else
						\space(\emph{\@email})
					\fi
				\end{center}
			\end{minipage}

			% Dół strony
			\vfill
			{\large \@data}
		\end{center}
	\end{titlepage}
	
	% Licznik strony
	\setcounter{page}{2}
}