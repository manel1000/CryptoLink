// controllers/statistiqueController.js
const statistiqueService = require('../services/statistiqueService') ;// This should now correctly find the updated service file

async function getStudentsPerPalierStats(req, res) {
    try {
        const stats = await statistiqueService.getStudentCountPerPalier();
        res.status(200).json({
            success: true,
            message: 'Student counts per palier fetched successfully.',
            data: stats
        });
    } catch (error) {
        console.error("Error in statisticsController > getStudentsPerPalierStats:", error);
        res.status(500).json({
            success: false,
            message: 'Failed to fetch student statistics per palier.',
            error: error.message
        });
    }
}

//  GET THE NBR OF STUDENTS PER SECTION 
async function getStudentsPerSectionStats(req, res) {
    try {
        const stats = await statistiqueService.getStudentCountPerSection();
        res.status(200).json({
            success: true,
            message: 'Student counts per section fetched successfully.',
            data: stats
        });
       }catch (error) {
        console.error("Error in statisticsController > getStudentsPerSectionStats:", error);
        res.status(500).json({
            success: false,
            message: 'Failed to fetch student statistics per section.',
            error: error.message
        });
    }
}


//Nouvelle fonction pour gérer la requête GET du nombre d'étudiants handicapés
async function handleGetHandicapedCount(req, res) {
    try {
        const count = await statistiqueService.getHandicapedStudentCount();
        res.status(200).json({
            success: true,
            message: 'Nombre d\'étudiants handicapés récupéré avec succès.',
            data: { totalHandicaped: count } // Renvoie le compte dans un objet data
        });
    } catch (error) {
        console.error("Error in statistiqueController > handleGetHandicapedCount:", error);
        res.status(500).json({
            success: false,
            message: 'Échec de la récupération du nombre d\'étudiants handicapés.',
            error: error.message
        });
    }
}

//  exporter cette les fonctions de contrôleur

module.exports = {
    getStudentsPerPalierStats,
    getStudentsPerSectionStats, 
    handleGetHandicapedCount
};
